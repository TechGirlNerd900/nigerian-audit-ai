from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

class RiskLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"

class RiskCategory(str, Enum):
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    MARKET = "market"
    CREDIT = "credit"
    STRATEGIC = "strategic"
    REPUTATIONAL = "reputational"

class RiskImpact(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class RiskProbability(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class CompanyInfo(BaseModel):
    name: str = Field(..., description="Company name")
    industry: str = Field(..., description="Industry sector")
    size: str = Field("medium", description="Company size: small, medium, large")
    type: str = Field("private", description="Company type")
    location: Optional[str] = Field(None, description="Primary business location")
    employees: Optional[int] = Field(None, description="Number of employees")
    founded_year: Optional[int] = Field(None, description="Year company was founded")
    
    @validator('size')
    def validate_size(cls, v):
        valid_sizes = ['small', 'medium', 'large']
        if v.lower() not in valid_sizes:
            raise ValueError(f'Size must be one of {valid_sizes}')
        return v.lower()

class FinancialData(BaseModel):
    annual_revenue: float = Field(..., description="Annual revenue in NGN")
    total_assets: float = Field(..., description="Total assets in NGN")
    total_liabilities: float = Field(..., description="Total liabilities in NGN")
    current_assets: Optional[float] = Field(None, description="Current assets in NGN")
    current_liabilities: Optional[float] = Field(None, description="Current liabilities in NGN")
    cash_and_equivalents: Optional[float] = Field(None, description="Cash and cash equivalents in NGN")
    net_income: Optional[float] = Field(None, description="Net income in NGN")
    ebitda: Optional[float] = Field(None, description="EBITDA in NGN")
    debt_to_equity_ratio: Optional[float] = Field(None, description="Debt-to-equity ratio")
    current_ratio: Optional[float] = Field(None, description="Current ratio")
    quick_ratio: Optional[float] = Field(None, description="Quick ratio")
    return_on_assets: Optional[float] = Field(None, description="Return on assets")
    return_on_equity: Optional[float] = Field(None, description="Return on equity")
    
    @validator('annual_revenue', 'total_assets', 'total_liabilities')
    def validate_positive_amounts(cls, v):
        if v < 0:
            raise ValueError('Financial amounts must be positive')
        return v

class HistoricalData(BaseModel):
    years_of_data: int = Field(..., description="Number of years of historical data")
    revenue_growth_rate: Optional[float] = Field(None, description="Average annual revenue growth rate")
    profit_margin_trend: Optional[str] = Field(None, description="Profit margin trend: improving, stable, declining")
    debt_trend: Optional[str] = Field(None, description="Debt trend: increasing, stable, decreasing")
    market_share_trend: Optional[str] = Field(None, description="Market share trend")
    previous_audit_findings: Optional[List[str]] = Field(None, description="Previous audit findings")
    regulatory_violations: Optional[List[str]] = Field(None, description="Previous regulatory violations")

class RiskFactor(BaseModel):
    category: RiskCategory
    name: str = Field(..., description="Risk factor name")
    description: str = Field(..., description="Risk factor description")
    impact: RiskImpact
    probability: RiskProbability
    score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    mitigation_measures: Optional[List[str]] = Field(None, description="Current mitigation measures")
    recommendations: Optional[List[str]] = Field(None, description="Risk mitigation recommendations")

class RiskAssessmentResult(BaseModel):
    overall_risk_score: float = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    overall_risk_level: RiskLevel
    risk_factors: List[RiskFactor]
    critical_risks: List[Dict[str, Any]]
    risk_matrix: List[Dict[str, Any]]
    mitigation_strategies: List[str]
    recommendations: List[str]
    monitoring_requirements: Optional[List[str]] = Field(None, description="Risk monitoring requirements")
    next_review_date: Optional[str] = Field(None, description="Next risk review date")

class RiskAssessmentRequest(BaseModel):
    company_info: CompanyInfo
    financial_data: FinancialData
    historical_data: Optional[HistoricalData] = Field(None, description="Historical performance data")
    risk_categories: List[RiskCategory] = Field(
        default=[RiskCategory.FINANCIAL, RiskCategory.OPERATIONAL, RiskCategory.COMPLIANCE],
        description="Risk categories to assess"
    )
    assessment_scope: Optional[str] = Field("comprehensive", description="Assessment scope")
    assessment_purpose: Optional[str] = Field(None, description="Purpose of risk assessment")
    
    @validator('risk_categories')
    def validate_risk_categories(cls, v):
        if not v:
            raise ValueError('At least one risk category must be specified')
        return v

class RiskAssessmentResponse(BaseModel):
    success: bool = Field(True, description="Whether the assessment was successful")
    data: Optional[RiskAssessmentResult] = Field(None, description="Risk assessment results")
    error: Optional[str] = Field(None, description="Error message if assessment failed")
    timestamp: Optional[str] = Field(None, description="Assessment timestamp")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

class RiskScenario(BaseModel):
    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    probability: RiskProbability
    impact_factors: Dict[str, float] = Field(..., description="Impact on different risk factors")
    assumptions: List[str] = Field(..., description="Scenario assumptions")

class RiskScenarioAnalysisRequest(BaseModel):
    base_assessment: RiskAssessmentRequest
    scenarios: List[RiskScenario]
    include_base_case: bool = Field(True, description="Include base case in results")

class RiskScenarioResult(BaseModel):
    scenario_name: str
    risk_score_change: float = Field(..., description="Change in risk score from base case")
    affected_categories: List[RiskCategory]
    key_impacts: List[str]
    mitigation_adjustments: List[str]

class RiskScenarioAnalysisResponse(BaseModel):
    success: bool = Field(True, description="Whether the analysis was successful")
    base_case: Optional[RiskAssessmentResult] = Field(None, description="Base case assessment")
    scenario_results: List[RiskScenarioResult] = Field([], description="Scenario analysis results")
    comparative_summary: Optional[Dict[str, Any]] = Field(None, description="Comparative analysis summary")
    timestamp: Optional[str] = Field(None, description="Analysis timestamp")

class RiskMonitoringIndicator(BaseModel):
    name: str = Field(..., description="Indicator name")
    category: RiskCategory
    description: str = Field(..., description="Indicator description")
    current_value: Optional[float] = Field(None, description="Current indicator value")
    threshold_values: Dict[str, float] = Field(..., description="Threshold values for different risk levels")
    frequency: str = Field(..., description="Monitoring frequency")
    data_source: str = Field(..., description="Data source for indicator")

class RiskMonitoringPlan(BaseModel):
    company_name: str
    plan_effective_date: str
    review_frequency: str = Field("quarterly", description="Plan review frequency")
    key_risk_indicators: List[RiskMonitoringIndicator]
    escalation_procedures: List[str]
    reporting_requirements: List[str]
    responsible_parties: Dict[str, str] = Field(..., description="Responsible parties for each risk category")

class RiskToleranceLevel(BaseModel):
    category: RiskCategory
    tolerance_level: RiskLevel
    rationale: str = Field(..., description="Rationale for tolerance level")
    review_frequency: str = Field("annually", description="Review frequency for tolerance level")

class RiskAppetiteStatement(BaseModel):
    company_name: str
    effective_date: str
    tolerance_levels: List[RiskToleranceLevel]
    overall_risk_philosophy: str = Field(..., description="Overall risk management philosophy")
    board_approval_date: Optional[str] = Field(None, description="Board approval date")
    next_review_date: str = Field(..., description="Next review date")

class IndustryRiskBenchmark(BaseModel):
    industry: str
    risk_category: RiskCategory
    low_threshold: float = Field(..., ge=0, le=100)
    medium_threshold: float = Field(..., ge=0, le=100)
    high_threshold: float = Field(..., ge=0, le=100)
    average_score: float = Field(..., ge=0, le=100)
    data_source: str = Field(..., description="Source of benchmark data")
    last_updated: str = Field(..., description="Last update date for benchmark")

class RiskTrendAnalysis(BaseModel):
    category: RiskCategory
    trend_direction: str = Field(..., description="improving, stable, deteriorating")
    trend_magnitude: str = Field(..., description="slight, moderate, significant")
    time_period: str = Field(..., description="Time period for trend analysis")
    key_drivers: List[str] = Field(..., description="Key drivers of the trend")
    implications: List[str] = Field(..., description="Implications of the trend")

class RiskAssessmentMetadata(BaseModel):
    assessment_id: str = Field(..., description="Unique assessment identifier")
    version: str = Field("1.0", description="Assessment version")
    assessor_name: Optional[str] = Field(None, description="Name of person conducting assessment")
    methodology: str = Field("Nigerian Audit AI Risk Framework", description="Assessment methodology")
    standards_used: List[str] = Field(["ISO 31000", "COSO ERM"], description="Risk management standards used")
    limitations: Optional[List[str]] = Field(None, description="Assessment limitations")
    confidence_level: Optional[float] = Field(None, ge=0, le=100, description="Confidence level in assessment")