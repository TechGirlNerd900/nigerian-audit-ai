from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from typing import Optional
from datetime import datetime, timedelta
import redis

from ..config.settings import settings
from ..models.financial_analyzer import FinancialAnalyzer
from ..models.compliance_checker import ComplianceChecker
from ..models.risk_assessor import RiskAssessor
from ..models.document_processor import DocumentProcessor
from ..config.database import get_redis

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Global model instances (initialized in main.py)
_financial_analyzer: Optional[FinancialAnalyzer] = None
_compliance_checker: Optional[ComplianceChecker] = None
_risk_assessor: Optional[RiskAssessor] = None
_document_processor: Optional[DocumentProcessor] = None

def set_global_models(financial_analyzer: FinancialAnalyzer, 
                     compliance_checker: ComplianceChecker,
                     risk_assessor: RiskAssessor,
                     document_processor: DocumentProcessor):
    """Set global model instances"""
    global _financial_analyzer, _compliance_checker, _risk_assessor, _document_processor
    _financial_analyzer = financial_analyzer
    _compliance_checker = compliance_checker
    _risk_assessor = risk_assessor
    _document_processor = document_processor

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify API key authentication"""
    
    api_key = credentials.credentials
    
    # Check against configured API key
    if api_key != settings.API_KEY:
        logger.warning(f"Invalid API key attempt: {api_key[:8]}...")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return api_key

async def check_rate_limit(request: Request, api_key: str = Depends(verify_api_key)):
    """Check API rate limiting"""
    
    redis_client = get_redis()
    
    if redis_client is None:
        # No Redis, skip rate limiting
        return
    
    try:
        # Create rate limit key
        client_ip = request.client.host
        rate_limit_key = f"rate_limit:{api_key}:{client_ip}"
        
        # Get current request count
        current_requests = redis_client.get(rate_limit_key)
        
        if current_requests is None:
            # First request in window
            redis_client.setex(rate_limit_key, 60, 1)  # 1 minute window
        else:
            current_count = int(current_requests)
            
            if current_count >= 100:  # 100 requests per minute
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Maximum 100 requests per minute.",
                    headers={"Retry-After": "60"}
                )
            
            # Increment counter
            redis_client.incr(rate_limit_key)
    
    except redis.RedisError as e:
        logger.warning(f"Redis rate limiting error: {e}")
        # Continue without rate limiting if Redis fails

def get_financial_analyzer() -> FinancialAnalyzer:
    """Get financial analyzer instance"""
    if _financial_analyzer is None:
        raise HTTPException(
            status_code=503,
            detail="Financial analyzer not available"
        )
    return _financial_analyzer

def get_compliance_checker() -> ComplianceChecker:
    """Get compliance checker instance"""
    if _compliance_checker is None:
        raise HTTPException(
            status_code=503,
            detail="Compliance checker not available"
        )
    return _compliance_checker

def get_risk_assessor() -> RiskAssessor:
    """Get risk assessor instance"""
    if _risk_assessor is None:
        raise HTTPException(
            status_code=503,
            detail="Risk assessor not available"
        )
    return _risk_assessor

def get_document_processor() -> DocumentProcessor:
    """Get document processor instance"""
    if _document_processor is None:
        raise HTTPException(
            status_code=503,
            detail="Document processor not available"
        )
    return _document_processor

async def validate_nigerian_business_data(data: dict):
    """Validate Nigerian business identifiers"""
    
    from ..utils.validators import NigerianValidator
    
    validator = NigerianValidator()
    validation_errors = []
    
    # Validate CAC number if provided
    if 'cac_number' in data:
        cac_result = validator.validate_cac_number(data['cac_number'])
        if not cac_result['format_valid']:
            validation_errors.append("Invalid CAC number format")
    
    # Validate TIN if provided
    if 'tin_number' in data:
        tin_result = validator.validate_tin_number(data['tin_number'])
        if not tin_result['format_valid']:
            validation_errors.append("Invalid TIN format")
    
    # Validate phone number if provided
    if 'phone' in data:
        phone_result = validator.validate_phone_number(data['phone'])
        if not phone_result['valid']:
            validation_errors.append("Invalid Nigerian phone number format")
    
    if validation_errors:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Validation errors found",
                "errors": validation_errors
            }
        )

async def log_api_request(request: Request, api_key: str = Depends(verify_api_key)):
    """Log API requests for audit trail"""
    
    try:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": str(request.url.path),
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "api_key_hash": hash(api_key)  # Don't log actual API key
        }
        
        logger.info(f"API request: {log_data}")
        
    except Exception as e:
        logger.error(f"Failed to log API request: {e}")

class RequestTimer:
    """Dependency to time request processing"""
    
    def __init__(self):
        self.start_time = datetime.utcnow()
    
    def get_duration(self) -> float:
        """Get request duration in seconds"""
        return (datetime.utcnow() - self.start_time).total_seconds()

def get_request_timer() -> RequestTimer:
    """Get request timer instance"""
    return RequestTimer()

async def check_maintenance_mode():
    """Check if system is in maintenance mode"""
    
    # This could check a database flag or environment variable
    maintenance_mode = False  # Could be set via environment variable
    
    if maintenance_mode:
        raise HTTPException(
            status_code=503,
            detail="System is currently under maintenance. Please try again later.",
            headers={"Retry-After": "3600"}  # 1 hour
        )

async def validate_request_size(request: Request):
    """Validate request size limits"""
    
    # Check content length
    content_length = request.headers.get("content-length")
    
    if content_length:
        size_mb = int(content_length) / (1024 * 1024)
        
        if size_mb > 10:  # 10MB limit
            raise HTTPException(
                status_code=413,
                detail="Request payload too large. Maximum size is 10MB."
            )

def get_pagination_params(page: int = 1, size: int = 20):
    """Get pagination parameters with validation"""
    
    if page < 1:
        raise HTTPException(status_code=422, detail="Page must be >= 1")
    
    if size < 1 or size > 100:
        raise HTTPException(status_code=422, detail="Size must be between 1 and 100")
    
    offset = (page - 1) * size
    
    return {"offset": offset, "limit": size, "page": page, "size": size}

async def check_feature_flag(feature: str) -> bool:
    """Check if a feature is enabled"""
    
    # Feature flags could be stored in database or environment variables
    feature_flags = {
        "document_processing": True,
        "advanced_analytics": True,
        "ml_predictions": True,
        "real_time_validation": False
    }
    
    return feature_flags.get(feature, False)

async def get_client_info(request: Request) -> dict:
    """Extract client information from request"""
    
    return {
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent", ""),
        "referer": request.headers.get("referer", ""),
        "accept_language": request.headers.get("accept-language", ""),
        "timestamp": datetime.utcnow().isoformat()
    }