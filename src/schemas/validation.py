from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from enum import Enum

class ValidationType(str, Enum):
    CAC_NUMBER = "cac_number"
    TIN_NUMBER = "tin_number"
    PHONE_NUMBER = "phone_number"
    EMAIL_ADDRESS = "email_address"
    NIGERIAN_ADDRESS = "nigerian_address"
    BUSINESS_TYPE = "business_type"
    INDUSTRY_SECTOR = "industry_sector"
    BANK_ACCOUNT = "bank_account"
    BVN = "bvn"
    COMPANY_DATA = "company_data"
    FINANCIAL_DATA = "financial_data"

class ValidationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ValidationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    PARTIALLY_VALID = "partially_valid"
    REQUIRES_VERIFICATION = "requires_verification"
    UNKNOWN = "unknown"

class ValidationIssue(BaseModel):
    field: str = Field(..., description="Field name with issue")
    issue_type: str = Field(..., description="Type of validation issue")
    message: str = Field(..., description="Detailed issue message")
    severity: ValidationSeverity
    suggestion: Optional[str] = Field(None, description="Suggested correction")
    code: Optional[str] = Field(None, description="Error code for programmatic handling")

class ValidationResult(BaseModel):
    field_name: str = Field(..., description="Name of validated field")
    validation_type: ValidationType
    status: ValidationStatus
    is_valid: bool = Field(..., description="Overall validation result")
    confidence_score: float = Field(..., ge=0, le=100, description="Confidence in validation result")
    issues: List[ValidationIssue] = Field([], description="List of validation issues")
    suggestions: List[str] = Field([], description="Improvement suggestions")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional validation metadata")

class CompanyValidationData(BaseModel):
    name: str = Field(..., description="Company name")
    cac_number: Optional[str] = Field(None, description="CAC registration number")
    tin_number: Optional[str] = Field(None, description="Tax identification number")
    business_type: Optional[str] = Field(None, description="Type of business entity")
    industry: Optional[str] = Field(None, description="Industry sector")
    address: Optional[str] = Field(None, description="Business address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[str] = Field(None, description="Contact email address")
    website: Optional[str] = Field(None, description="Company website")
    is_public: bool = Field(False, description="Whether company is publicly listed")
    incorporation_date: Optional[str] = Field(None, description="Date of incorporation")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Company name must be at least 2 characters')
        return v.strip()

class FinancialValidationData(BaseModel):
    trial_balance: Dict[str, float] = Field(..., description="Trial balance data")
    revenue: Optional[float] = Field(None, description="Annual revenue")
    total_assets: Optional[float] = Field(None, description="Total assets")
    total_liabilities: Optional[float] = Field(None, description="Total liabilities")
    equity: Optional[float] = Field(None, description="Total equity")
    cash: Optional[float] = Field(None, description="Cash and cash equivalents")
    current_assets: Optional[float] = Field(None, description="Current assets")
    current_liabilities: Optional[float] = Field(None, description="Current liabilities")
    
    @validator('trial_balance')
    def validate_trial_balance(cls, v):
        if not v:
            raise ValueError('Trial balance cannot be empty')
        if not isinstance(v, dict):
            raise ValueError('Trial balance must be a dictionary')
        return v

class CompanyValidationRequest(BaseModel):
    company_data: CompanyValidationData
    validation_scope: List[ValidationType] = Field(
        default=[ValidationType.CAC_NUMBER, ValidationType.TIN_NUMBER, ValidationType.PHONE_NUMBER],
        description="Types of validation to perform"
    )
    verify_with_apis: bool = Field(False, description="Whether to verify with external APIs")
    strict_validation: bool = Field(False, description="Whether to use strict validation rules")
    
    @validator('validation_scope')
    def validate_scope(cls, v):
        if not v:
            raise ValueError('At least one validation type must be specified')
        return v

class FinancialDataValidationRequest(BaseModel):
    financial_data: FinancialValidationData
    validation_rules: List[str] = Field(
        default=["accounting_equation", "positive_amounts", "ratio_reasonableness"],
        description="Financial validation rules to apply"
    )
    tolerance_percentage: float = Field(1.0, ge=0, le=10, description="Tolerance percentage for balance checks")

class BatchValidationItem(BaseModel):
    item_id: str = Field(..., description="Unique identifier for the item")
    validation_type: ValidationType
    data: Any = Field(..., description="Data to validate")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class BatchValidationRequest(BaseModel):
    items: List[BatchValidationItem] = Field(..., description="Items to validate")
    fail_fast: bool = Field(False, description="Stop on first error")
    parallel_processing: bool = Field(True, description="Process items in parallel")
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('At least one item must be provided for validation')
        if len(v) > 1000:
            raise ValueError('Maximum 1000 items allowed per batch')
        return v

class ValidationConfiguration(BaseModel):
    strict_mode: bool = Field(False, description="Enable strict validation")
    api_verification: bool = Field(False, description="Enable API verification")
    timeout_seconds: int = Field(30, ge=1, le=300, description="Validation timeout")
    cache_results: bool = Field(True, description="Cache validation results")
    include_suggestions: bool = Field(True, description="Include improvement suggestions")

class NigerianSpecificValidation(BaseModel):
    validate_cac_format: bool = Field(True, description="Validate CAC number format")
    validate_tin_format: bool = Field(True, description="Validate TIN format")
    validate_phone_format: bool = Field(True, description="Validate Nigerian phone format")
    validate_state_codes: bool = Field(True, description="Validate Nigerian state codes")
    validate_postal_codes: bool = Field(True, description="Validate Nigerian postal codes")
    validate_bank_codes: bool = Field(False, description="Validate Nigerian bank codes")

class ValidationSummary(BaseModel):
    total_validations: int = Field(..., description="Total number of validations performed")
    successful_validations: int = Field(..., description="Number of successful validations")
    failed_validations: int = Field(..., description="Number of failed validations")
    warnings_count: int = Field(..., description="Number of warnings")
    errors_count: int = Field(..., description="Number of errors")
    overall_score: float = Field(..., ge=0, le=100, description="Overall validation score")
    processing_time: float = Field(..., description="Total processing time in seconds")

class ValidationResponse(BaseModel):
    success: bool = Field(True, description="Whether validation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Validation results")
    summary: Optional[ValidationSummary] = Field(None, description="Validation summary")
    error: Optional[str] = Field(None, description="Error message if validation failed")
    timestamp: Optional[str] = Field(None, description="Validation timestamp")

class CAC_ValidationResult(BaseModel):
    cac_number: str = Field(..., description="CAC number that was validated")
    format_valid: bool = Field(..., description="Whether format is valid")
    company_type: Optional[str] = Field(None, description="Type of registration (RC, BN, IT)")
    existence_verified: bool = Field(False, description="Whether existence was verified")
    company_name: Optional[str] = Field(None, description="Company name from CAC database")
    registration_date: Optional[str] = Field(None, description="Registration date")
    status: Optional[str] = Field(None, description="Company status (active, inactive)")
    last_verified: Optional[str] = Field(None, description="Last verification date")

class TIN_ValidationResult(BaseModel):
    tin_number: str = Field(..., description="TIN number that was validated")
    format_valid: bool = Field(..., description="Whether format is valid")
    firs_verified: bool = Field(False, description="Whether verified with FIRS")
    taxpayer_name: Optional[str] = Field(None, description="Taxpayer name from FIRS")
    taxpayer_type: Optional[str] = Field(None, description="Type of taxpayer")
    tax_office: Optional[str] = Field(None, description="Assigned tax office")
    registration_date: Optional[str] = Field(None, description="TIN registration date")
    status: Optional[str] = Field(None, description="TIN status")

class PhoneValidationResult(BaseModel):
    phone_number: str = Field(..., description="Phone number that was validated")
    format_valid: bool = Field(..., description="Whether format is valid")
    country_code: Optional[str] = Field(None, description="Country code")
    network_provider: Optional[str] = Field(None, description="Network provider")
    line_type: Optional[str] = Field(None, description="Line type (mobile, landline)")
    formatted_number: Optional[str] = Field(None, description="Properly formatted number")

class EmailValidationResult(BaseModel):
    email_address: str = Field(..., description="Email address that was validated")
    format_valid: bool = Field(..., description="Whether format is valid")
    domain_valid: bool = Field(..., description="Whether domain is valid")
    is_corporate_email: bool = Field(..., description="Whether appears to be corporate email")
    domain_info: Optional[Dict[str, Any]] = Field(None, description="Domain information")

class AddressValidationResult(BaseModel):
    address: str = Field(..., description="Address that was validated")
    format_valid: bool = Field(..., description="Whether format is valid")
    components: Dict[str, str] = Field({}, description="Extracted address components")
    state_valid: bool = Field(..., description="Whether state is valid Nigerian state")
    postal_code_valid: bool = Field(..., description="Whether postal code is valid")
    formatted_address: Optional[str] = Field(None, description="Properly formatted address")

class BusinessTypeValidationResult(BaseModel):
    business_type: str = Field(..., description="Business type that was validated")
    is_valid_type: bool = Field(..., description="Whether is valid Nigerian business type")
    matches_cac_pattern: bool = Field(..., description="Whether matches CAC registration pattern")
    standardized_type: Optional[str] = Field(None, description="Standardized business type name")
    required_registrations: List[str] = Field([], description="Required registrations for this type")

class IndustryValidationResult(BaseModel):
    industry: str = Field(..., description="Industry that was validated")
    is_valid_industry: bool = Field(..., description="Whether is recognized industry")
    standardized_industry: Optional[str] = Field(None, description="Standardized industry name")
    industry_code: Optional[str] = Field(None, description="Industry classification code")
    regulatory_requirements: List[str] = Field([], description="Industry-specific regulatory requirements")

class FinancialDataValidationResult(BaseModel):
    accounting_equation_balanced: bool = Field(..., description="Whether accounting equation balances")
    balance_difference: float = Field(0.0, description="Difference in accounting equation")
    ratio_anomalies: List[str] = Field([], description="Detected ratio anomalies")
    negative_value_issues: List[str] = Field([], description="Inappropriate negative values")
    consistency_checks: Dict[str, bool] = Field({}, description="Various consistency check results")
    data_quality_score: float = Field(..., ge=0, le=100, description="Overall data quality score")

class ValidationPattern(BaseModel):
    pattern_name: str = Field(..., description="Name of validation pattern")
    pattern_type: ValidationType
    regex_pattern: str = Field(..., description="Regular expression pattern")
    description: str = Field(..., description="Pattern description")
    examples: List[str] = Field([], description="Valid examples")
    error_message: str = Field(..., description="Error message for invalid input")

class ValidationRule(BaseModel):
    rule_name: str = Field(..., description="Name of validation rule")
    rule_type: str = Field(..., description="Type of validation rule")
    condition: str = Field(..., description="Rule condition")
    error_message: str = Field(..., description="Error message when rule fails")
    severity: ValidationSeverity
    is_active: bool = Field(True, description="Whether rule is active")

class ValidationRequest(BaseModel):
    validation_type: ValidationType
    data: Any = Field(..., description="Data to validate")
    configuration: Optional[ValidationConfiguration] = Field(None, description="Validation configuration")
    nigerian_specific: Optional[NigerianSpecificValidation] = Field(None, description="Nigerian-specific settings")
    custom_rules: Optional[List[ValidationRule]] = Field(None, description="Custom validation rules")