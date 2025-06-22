from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from decimal import Decimal

class TrialBalanceAccount(BaseModel):
    account_name: str = Field(..., description="Name of the account")
    amount: float = Field(..., description="Account balance in Nigerian Naira")
    account_code: Optional[str] = Field(None, description="Chart of accounts code")
    
    @validator('amount')
    def validate_amount(cls, v):
        if not isinstance(v, (int, float, Decimal)):
            raise ValueError('Amount must be a number')
        if v < -999_999_999_999 or v > 999_999_999_999:
            raise ValueError('Amount out of reasonable range')
        return float(v)

class CompanyInfo(BaseModel):
    name: Optional[str] = Field(None, description="Company name")
    type: str = Field("general", description="Company type: manufacturing, banking, oil_gas, etc.")
    size: str = Field("medium", description="Company size: small, medium, large")
    industry: Optional[str] = Field(None, description="Industry classification")
    cac_number: Optional[str] = Field(None, description="CAC registration number")
    tin_number: Optional[str] = Field(None, description="Tax identification number")
    employee_count: Optional[int] = Field(None, description="Number of employees")
    annual_revenue: Optional[float] = Field(None, description="Annual revenue in NGN")
    is_public: bool = Field(False, description="Is the company publicly listed")

class FinancialAnalysisRequest(BaseModel):
    trial_balance: Dict[str, float] = Field(..., description="Trial balance accounts and amounts")
    company_info: Optional[CompanyInfo] = Field(None, description="Company information")
    analysis_type: str = Field("comprehensive", description="Type of analysis: basic, comprehensive, detailed")
    prior_period_data: Optional[Dict[str, float]] = Field(None, description="Prior period data for comparison")
    
    @validator('trial_balance')
    def validate_trial_balance(cls, v):
        if not v:
            raise ValueError('Trial balance cannot be empty')
        if len(v) < 3:
            raise ValueError('Trial balance must have at least 3 accounts')
        return v

class FinancialRatios(BaseModel):
    # Liquidity Ratios
    current_ratio: float = Field(0.0, description="Current assets / Current liabilities")
    quick_ratio: float = Field(0.0, description="Quick assets / Current liabilities")
    cash_ratio: float = Field(0.0, description="Cash / Current liabilities")
    
    # Leverage Ratios
    debt_to_equity: float = Field(0.0, description="Total debt / Total equity")
    debt_to_assets: float = Field(0.0, description="Total debt / Total assets")
    equity_ratio: float = Field(0.0, description="Total equity / Total assets")
    
    # Profitability Ratios
    gross_profit_margin: float = Field(0.0, description="Gross profit / Revenue")
    net_profit_margin: float = Field(0.0, description="Net income / Revenue")
    return_on_assets: float = Field(0.0, description="Net income / Total assets")
    return_on_equity: float = Field(0.0, description="Net income / Total equity")
    
    # Activity Ratios
    asset_turnover: float = Field(0.0, description="Revenue / Total assets")
    inventory_turnover: float = Field(0.0, description="Cost of sales / Average inventory")
    receivables_turnover: float = Field(0.0, description="Revenue / Average receivables")

class FinancialAssessment(BaseModel):
    overall_score: float = Field(..., description="Overall financial health score (0-100)")
    risk_level: str = Field(..., description="Risk level: LOW, MEDIUM, HIGH, CRITICAL")
    strengths: List[str] = Field([], description="Financial strengths identified")
    weaknesses: List[str] = Field([], description="Financial weaknesses identified")
    recommendations: List[str] = Field([], description="Recommendations for improvement")
    compliance_flags: List[str] = Field([], description="Nigerian compliance issues")

class AccountClassification(BaseModel):
    current_assets: Dict[str, str] = Field({}, description="Current assets with NGN formatting")
    non_current_assets: Dict[str, str] = Field({}, description="Non-current assets with NGN formatting")
    current_liabilities: Dict[str, str] = Field({}, description="Current liabilities with NGN formatting")
    non_current_liabilities: Dict[str, str] = Field({}, description="Non-current liabilities with NGN formatting")
    equity: Dict[str, str] = Field({}, description="Equity accounts with NGN formatting")
    revenue: Dict[str, str] = Field({}, description="Revenue accounts with NGN formatting")
    expenses: Dict[str, str] = Field({}, description="Expense accounts with NGN formatting")

class FinancialSummary(BaseModel):
    total_assets: str = Field(..., description="Total assets in NGN format")
    total_liabilities: str = Field(..., description="Total liabilities in NGN format")
    total_equity: str = Field(..., description="Total equity in NGN format")
    net_income: str = Field(..., description="Net income in NGN format")

class FinancialAnalysisData(BaseModel):
    classification: AccountClassification
    ratios: FinancialRatios
    assessment: FinancialAssessment
    summary: FinancialSummary

class FinancialAnalysisResponse(BaseModel):
    success: bool = Field(True, description="Whether the analysis was successful")
    data: Optional[FinancialAnalysisData] = Field(None, description="Analysis results")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    timestamp: Optional[str] = Field(None, description="Analysis timestamp")

