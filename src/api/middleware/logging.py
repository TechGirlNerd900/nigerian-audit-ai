import logging
import time
import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses"""
    
    def __init__(self, app, log_level: str = "INFO"):
        super().__init__(app)
        self.log_level = getattr(logging, log_level.upper())
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing
        start_time = time.time()
        
        # Extract request info
        request_info = await self._extract_request_info(request)
        
        # Log request
        if logger.isEnabledFor(self.log_level):
            logger.log(self.log_level, f"Request started: {request_info}")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Extract response info
            response_info = self._extract_response_info(response, process_time)
            
            # Log response
            if logger.isEnabledFor(self.log_level):
                logger.log(self.log_level, f"Request completed: {response_info}")
            
            # Add processing time header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Calculate processing time for failed requests
            process_time = time.time() - start_time
            
            # Log error
            error_info = {
                **request_info,
                "error": str(e),
                "process_time": process_time,
                "status": "error"
            }
            
            logger.error(f"Request failed: {error_info}")
            raise
    
    async def _extract_request_info(self, request: Request) -> dict:
        """Extract relevant request information"""
        
        # Get client IP (handle proxies)
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        request_info = {
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": client_ip,
            "user_agent": request.headers.get("User-Agent", ""),
            "content_type": request.headers.get("Content-Type", ""),
            "content_length": request.headers.get("Content-Length", "0"),
            "authorization": "Bearer ***" if request.headers.get("Authorization") else None,
            "timestamp": time.time()
        }
        
        # Exclude sensitive paths from detailed logging
        sensitive_paths = ["/docs", "/openapi.json", "/health"]
        if request.url.path not in sensitive_paths:
            try:
                # Log request body for POST/PUT requests (limited size)
                if request.method in ["POST", "PUT", "PATCH"]:
                    content_length = int(request_info["content_length"] or 0)
                    if content_length > 0 and content_length < 10240:  # 10KB limit
                        body = await request.body()
                        if body:
                            try:
                                # Try to parse as JSON
                                request_info["body"] = json.loads(body.decode())
                            except (json.JSONDecodeError, UnicodeDecodeError):
                                request_info["body"] = f"<binary data: {len(body)} bytes>"
            except Exception as e:
                logger.warning(f"Failed to log request body: {e}")
        
        return request_info
    
    def _extract_response_info(self, response: Response, process_time: float) -> dict:
        """Extract relevant response information"""
        
        response_info = {
            "status_code": response.status_code,
            "content_type": response.headers.get("Content-Type", ""),
            "content_length": response.headers.get("Content-Length", "0"),
            "process_time": round(process_time, 4),
            "timestamp": time.time()
        }
        
        # Add custom headers if present
        if "X-Request-ID" in response.headers:
            response_info["request_id"] = response.headers["X-Request-ID"]
        
        return response_info

class AuditLogMiddleware(BaseHTTPMiddleware):
    """Middleware for audit logging of sensitive operations"""
    
    def __init__(self, app):
        super().__init__(app)
        self.audit_paths = [
            "/api/v1/analyze",
            "/api/v1/compliance",
            "/api/v1/risk"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check if this is an auditable request
        if any(request.url.path.startswith(path) for path in self.audit_paths):
            await self._log_audit_event(request)
        
        response = await call_next(request)
        return response
    
    async def _log_audit_event(self, request: Request):
        """Log audit event for compliance tracking"""
        
        try:
            # Extract API key hash for tracking
            auth_header = request.headers.get("Authorization", "")
            api_key_hash = hash(auth_header) if auth_header else "anonymous"
            
            audit_data = {
                "event_type": "api_access",
                "endpoint": request.url.path,
                "method": request.method,
                "client_ip": request.client.host if request.client else "unknown",
                "api_key_hash": api_key_hash,
                "timestamp": time.time(),
                "user_agent": request.headers.get("User-Agent", "")
            }
            
            # Use a separate audit logger
            audit_logger = logging.getLogger("audit")
            audit_logger.info(json.dumps(audit_data))
            
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add unique request IDs for tracking"""
    
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        import uuid
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Add to request state for use in other middleware/endpoints
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response

class APIUsageMiddleware(BaseHTTPMiddleware):
    """Middleware to track API usage statistics"""
    
    def __init__(self, app):
        super().__init__(app)
        self.usage_stats = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Extract API key for usage tracking
        auth_header = request.headers.get("Authorization", "")
        api_key = "anonymous"
        
        if auth_header.startswith("Bearer "):
            api_key_full = auth_header[7:]
            api_key = api_key_full[:8] + "..." if len(api_key_full) > 8 else api_key_full
        
        # Track usage
        endpoint = request.url.path
        method = request.method
        usage_key = f"{api_key}:{method}:{endpoint}"
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Update usage statistics
        if usage_key not in self.usage_stats:
            self.usage_stats[usage_key] = {
                "count": 0,
                "total_time": 0,
                "avg_time": 0,
                "last_used": None
            }
        
        stats = self.usage_stats[usage_key]
        stats["count"] += 1
        stats["total_time"] += process_time
        stats["avg_time"] = stats["total_time"] / stats["count"]
        stats["last_used"] = time.time()
        
        # Add usage info to response headers
        response.headers["X-API-Usage-Count"] = str(stats["count"])
        response.headers["X-API-Avg-Time"] = str(round(stats["avg_time"], 4))
        
        return response
    
    def get_usage_stats(self) -> dict:
        """Get current usage statistics"""
        return self.usage_stats.copy()

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware to handle correlation IDs for distributed tracing"""
    
    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        import uuid
        
        # Check for existing correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        
        if not correlation_id:
            # Generate new correlation ID
            correlation_id = str(uuid.uuid4())
        
        # Store in request state
        request.state.correlation_id = correlation_id
        
        # Process request
        response = await call_next(request)
        
        # Add correlation ID to response
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response