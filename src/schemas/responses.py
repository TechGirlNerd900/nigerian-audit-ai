from pydantic import BaseModel, Field
from typing import Any, Optional, Dict, List
from datetime import datetime

class BaseResponse(BaseModel):
    """Base response model for all API endpoints"""
    success: bool = Field(True, description="Whether the operation was successful")
    message: Optional[str] = Field(None, description="Response message")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Response timestamp")

class SuccessResponse(BaseResponse):
    """Success response with data"""
    data: Any = Field(..., description="Response data")

class ErrorResponse(BaseResponse):
    """Error response model"""
    success: bool = Field(False, description="Always false for error responses")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

class ValidationErrorResponse(ErrorResponse):
    """Validation error response"""
    error_code: str = Field("VALIDATION_ERROR", description="Validation error code")
    validation_errors: List[Dict[str, str]] = Field([], description="Field validation errors")

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field("healthy", description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    models_loaded: Dict[str, bool] = Field({}, description="Status of loaded models")
    database_connected: bool = Field(True, description="Database connection status")
    cache_connected: bool = Field(True, description="Cache connection status")

class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")

class PaginatedResponse(BaseResponse):
    """Paginated response model"""
    data: List[Any] = Field(..., description="Paginated data items")
    meta: PaginationMeta = Field(..., description="Pagination metadata")

class NigerianValidationResponse(BaseResponse):
    """Nigerian data validation response"""
    validation_type: str = Field(..., description="Type of validation performed")
    valid: bool = Field(..., description="Whether the data is valid")
    format_valid: bool = Field(..., description="Whether the format is valid")
    api_verified: bool = Field(False, description="Whether API verification was successful")
    details: Dict[str, Any] = Field({}, description="Additional validation details")

class RiskAssessmentResponse(BaseResponse):
    """Risk assessment response"""
    risk_level: str = Field(..., description="Overall risk level")
    risk_score: float = Field(..., description="Risk score (0-100)")
    risk_factors: List[Dict[str, Any]] = Field([], description="Identified risk factors")
    mitigation_strategies: List[str] = Field([], description="Risk mitigation strategies")

class DocumentProcessingResponse(BaseResponse):
    """Document processing response"""
    document_type: str = Field(..., description="Type of processed document")
    extracted_data: Dict[str, Any] = Field({}, description="Extracted data from document")
    confidence_score: float = Field(..., description="Extraction confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")

class AsyncTaskResponse(BaseResponse):
    """Async task response"""
    task_id: str = Field(..., description="Task ID for tracking")
    status: str = Field("pending", description="Task status")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")
    progress: Optional[float] = Field(None, description="Task progress percentage")

class BulkOperationResponse(BaseResponse):
    """Bulk operation response"""
    total_items: int = Field(..., description="Total items processed")
    successful_items: int = Field(..., description="Successfully processed items")
    failed_items: int = Field(..., description="Failed items")
    errors: List[Dict[str, Any]] = Field([], description="List of errors encountered")
