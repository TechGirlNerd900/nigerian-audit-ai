from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from enum import Enum

class ComplianceRegulation(str, Enum):
    FRC = "FRC"  # Financial Reporting Council
    FIRS = "FIRS"  # Federal Inland Revenue Service
    CAMA = "CAMA"  # Companies and Allied Matters Act
    CBN = "CBN"  # Central Bank of Nigeria
    NGX = "NGX"  # Nigerian Exchange Group
    SEC = "SEC"  # Securities and Exchange Commission
    PENCOM = "PENCOM"  # National Pension Commission

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NOT_APPLICABLE = "not_applicable"
    REQUIRES_REVIEW = "requires_review"

class ViolationSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CompanyData(BaseModel):
    cac_number: str = Field(..., description="CAC registration number")
    tin_number: str = Field(..., description="Tax identification number")
    business_type: str = Field(..., description="Type of business entity")
    is_public: bool = Field(False, description="Whether company is publicly listed")
    industry_sector: Optional[str] = Field(None, description="Industry sector")
    incorporation_date: Optional[str] = Field(None, description="Date of incorporation")
    
    @validator('cac_number')
    def validate_cac_number(cls, v):
        import re
        if not re.match(r'^(RC|BN)\d{6,7}$', v.upper()):
            raise ValueError('Invalid CAC number format')
        return v.upper()
    
    @validator('tin_number')
    def validate_tin_number(cls, v):
        import re
        tin_clean = re.sub(r'\D', '', v)
        if len(tin_clean) != 12:
            raise ValueError('TIN must be 12 digits')
        return tin_clean

class FinancialData(BaseModel):
    annual_revenue: float = Field(..., description="Annual revenue in NGN")
    total_assets: float = Field(..., description="Total assets in NGN")
    total_liabilities: float = Field(..., description="Total liabilities in NGN")
    employee_count: Optional[int] = Field(None, description="Number of employees")
    financial_year_end: Optional[str] = Field(None, description="Financial year end date")

class ComplianceViolation(BaseModel):
    regulation: ComplianceRegulation
    violation_type: str = Field(..., description="Type of violation")
    description: str = Field(..., description="Description of the violation")
    severity: ViolationSeverity
    recommendation: str = Field(..., description="Recommended action")
    penalty_range: Optional[str] = Field(None, description="Potential penalty range")
    deadline: Optional[str] = Field(None, description="Compliance deadline")

class ComplianceCheckResult(BaseModel):
    regulation: ComplianceRegulation
    status: ComplianceStatus
    score: float = Field(..., description="Compliance score (0-100)")
    violations: List[ComplianceViolation] = Field([], description="List of violations")
    requirements_met: List[str] = Field([], description="Requirements that are met")
    missing_requirements: List[str] = Field([], description="Missing requirements")

class TaxComplianceDetails(BaseModel):
    vat_compliance: ComplianceStatus
    cit_compliance: ComplianceStatus
    paye_compliance: ComplianceStatus
    wht_compliance: ComplianceStatus
    estimated_tax_liability: Optional[float] = Field(None, description="Estimated tax liability in NGN")
    filing_status: str = Field("unknown", description="Tax filing status")

class FRCComplianceDetails(BaseModel):
    financial_statements_filed: bool = Field(False, description="Whether FS are filed")
    audit_compliance: ComplianceStatus
    disclosure_compliance: ComplianceStatus
    ifrs_compliance: ComplianceStatus
    corporate_governance: ComplianceStatus

class ComplianceCheckRequest(BaseModel):
    company_data: CompanyData
    financial_data: FinancialData
    regulations: List[ComplianceRegulation] = Field(..., description="Regulations to check")
    check_type: str = Field("standard", description="Type of compliance check")
    
    @validator('regulations')
    def validate_regulations(cls, v):
        if not v:
            raise ValueError('At least one regulation must be specified')
        return v

class ComplianceOverview(BaseModel):
    overall_status: ComplianceStatus
    overall_score: float = Field(..., description="Overall compliance score (0-100)")
    total_violations: int = Field(0, description="Total number of violations")
    critical_violations: int = Field(0, description="Number of critical violations")
    regulations_checked: List[ComplianceRegulation]
    last_updated: str = Field(..., description="Last update timestamp")

class ComplianceCheckData(BaseModel):
    overview: ComplianceOverview
    detailed_results: List[ComplianceCheckResult]
    tax_details: Optional[TaxComplianceDetails] = None
    frc_details: Optional[FRCComplianceDetails] = None
    recommendations: List[str] = Field([], description="Overall recommendations")
    action_items: List[str] = Field([], description="Immediate action items")

class ComplianceCheckResponse(BaseModel):
    success: bool = Field(True, description="Whether the check was successful")
    data: Optional[ComplianceCheckData] = Field(None, description="Compliance check results")
    error: Optional[str] = Field(None, description="Error message if check failed")
    timestamp: Optional[str] = Field(None, description="Check timestamp")
