from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import datetime

class ReportType(str, Enum):
    FINANCIAL_ANALYSIS = "financial_analysis"
    COMPLIANCE_ASSESSMENT = "compliance_assessment"
    RISK_ASSESSMENT = "risk_assessment"
    MANAGEMENT_LETTER = "management_letter"
    AUDIT_OPINION = "audit_opinion"
    EXECUTIVE_SUMMARY = "executive_summary"
    DETAILED_FINDINGS = "detailed_findings"
    BENCHMARKING_REPORT = "benchmarking_report"
    TREND_ANALYSIS = "trend_analysis"
    REGULATORY_UPDATE = "regulatory_update"

class ReportFormat(str, Enum):
    PDF = "pdf"
    WORD = "word"
    EXCEL = "excel"
    JSON = "json"
    HTML = "html"
    CSV = "csv"

class ReportScope(str, Enum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"
    EXECUTIVE = "executive"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CompanyInformation(BaseModel):
    name: str = Field(..., description="Company name")
    cac_number: Optional[str] = Field(None, description="CAC registration number")
    tin_number: Optional[str] = Field(None, description="Tax identification number")
    industry: Optional[str] = Field(None, description="Industry sector")
    business_type: Optional[str] = Field(None, description="Type of business entity")
    address: Optional[str] = Field(None, description="Business address")
    contact_person: Optional[str] = Field(None, description="Primary contact person")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[str] = Field(None, description="Contact email address")
    financial_year_end: Optional[str] = Field(None, description="Financial year end date")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Company name must be at least 2 characters')
        return v.strip()

class ReportConfiguration(BaseModel):
    include_charts: bool = Field(True, description="Include charts and graphs")
    include_appendices: bool = Field(True, description="Include detailed appendices")
    include_recommendations: bool = Field(True, description="Include recommendations")
    include_executive_summary: bool = Field(True, description="Include executive summary")
    include_comparative_analysis: bool = Field(False, description="Include comparative analysis")
    include_trend_analysis: bool = Field(False, description="Include trend analysis")
    confidentiality_level: str = Field("standard", description="Confidentiality level")
    branding: Optional[str] = Field(None, description="Custom branding options")

class ReportGenerationRequest(BaseModel):
    report_type: ReportType
    format: ReportFormat = Field(ReportFormat.PDF, description="Desired output format")
    scope: ReportScope = Field(ReportScope.DETAILED, description="Report scope")
    company_info: CompanyInformation
    analysis_data: Dict[str, Any] = Field({}, description="Analysis data for report")
    configuration: Optional[ReportConfiguration] = Field(None, description="Report configuration")
    custom_sections: Optional[List[str]] = Field(None, description="Custom sections to include")
    template_id: Optional[str] = Field(None, description="Custom template identifier")
    
    @validator('analysis_data')
    def validate_analysis_data(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Analysis data must be a dictionary')
        return v

class ReportSection(BaseModel):
    section_id: str = Field(..., description="Unique section identifier")
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")
    subsections: Optional[List['ReportSection']] = Field(None, description="Subsections")
    charts: Optional[List[Dict[str, Any]]] = Field(None, description="Charts and visualizations")
    tables: Optional[List[Dict[str, Any]]] = Field(None, description="Tables and data")
    page_break_before: bool = Field(False, description="Insert page break before section")
    confidential: bool = Field(False, description="Mark section as confidential")

class Finding(BaseModel):
    finding_id: str = Field(..., description="Unique finding identifier")
    title: str = Field(..., description="Finding title")
    description: str = Field(..., description="Detailed description")
    category: str = Field(..., description="Finding category")
    severity: Priority
    risk_level: str = Field(..., description="Associated risk level")
    current_status: str = Field(..., description="Current status")
    recommendation: str = Field(..., description="Recommended action")
    management_response: Optional[str] = Field(None, description="Management response")
    target_date: Optional[str] = Field(None, description="Target resolution date")
    responsible_party: Optional[str] = Field(None, description="Responsible party")

class Recommendation(BaseModel):
    recommendation_id: str = Field(..., description="Unique recommendation identifier")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed description")
    priority: Priority
    category: str = Field(..., description="Recommendation category")
    implementation_effort: str = Field(..., description="Implementation effort level")
    expected_benefit: str = Field(..., description="Expected benefit")
    timeline: str = Field(..., description="Recommended timeline")
    resources_required: Optional[List[str]] = Field(None, description="Required resources")
    success_metrics: Optional[List[str]] = Field(None, description="Success metrics")

class KeyMetric(BaseModel):
    metric_name: str = Field(..., description="Metric name")
    current_value: Union[float, str] = Field(..., description="Current metric value")
    previous_value: Optional[Union[float, str]] = Field(None, description="Previous period value")
    benchmark_value: Optional[Union[float, str]] = Field(None, description="Benchmark value")
    trend: Optional[str] = Field(None, description="Trend direction")
    variance: Optional[float] = Field(None, description="Variance from benchmark")
    interpretation: Optional[str] = Field(None, description="Metric interpretation")

class ExecutiveSummary(BaseModel):
    overall_assessment: str = Field(..., description="Overall assessment")
    key_highlights: List[str] = Field(..., description="Key highlights")
    major_concerns: List[str] = Field([], description="Major concerns")
    critical_recommendations: List[str] = Field([], description="Critical recommendations")
    conclusion: str = Field(..., description="Executive conclusion")

class FinancialAnalysisReport(BaseModel):
    company_info: CompanyInformation
    executive_summary: ExecutiveSummary
    financial_position: Dict[str, Any] = Field({}, description="Financial position analysis")
    performance_analysis: Dict[str, Any] = Field({}, description="Performance analysis")
    ratio_analysis: Dict[str, float] = Field({}, description="Financial ratios")
    trend_analysis: Optional[Dict[str, Any]] = Field(None, description="Trend analysis")
    benchmark_comparison: Optional[Dict[str, Any]] = Field(None, description="Benchmark comparison")
    risk_assessment: Dict[str, Any] = Field({}, description="Risk assessment results")
    key_metrics: List[KeyMetric] = Field([], description="Key financial metrics")
    findings: List[Finding] = Field([], description="Analysis findings")
    recommendations: List[Recommendation] = Field([], description="Recommendations")

class ComplianceAssessmentReport(BaseModel):
    company_info: CompanyInformation
    executive_summary: ExecutiveSummary
    compliance_overview: Dict[str, Any] = Field({}, description="Compliance overview")
    regulatory_framework: Dict[str, Any] = Field({}, description="Applicable regulatory framework")
    detailed_findings: List[Finding] = Field([], description="Compliance findings")
    violations_summary: Dict[str, Any] = Field({}, description="Summary of violations")
    remediation_plan: List[Recommendation] = Field([], description="Remediation plan")
    compliance_score: float = Field(..., ge=0, le=100, description="Overall compliance score")
    risk_areas: List[str] = Field([], description="High-risk compliance areas")

class RiskAssessmentReport(BaseModel):
    company_info: CompanyInformation
    executive_summary: ExecutiveSummary
    risk_profile: Dict[str, Any] = Field({}, description="Overall risk profile")
    risk_categories: Dict[str, Any] = Field({}, description="Risk by category")
    risk_matrix: List[Dict[str, Any]] = Field([], description="Risk matrix")
    critical_risks: List[Dict[str, Any]] = Field([], description="Critical risks")
    mitigation_strategies: List[Recommendation] = Field([], description="Risk mitigation strategies")
    monitoring_plan: Dict[str, Any] = Field({}, description="Risk monitoring plan")
    risk_appetite: Optional[Dict[str, Any]] = Field(None, description="Risk appetite statement")

class ManagementLetter(BaseModel):
    company_info: CompanyInformation
    addressee: str = Field(..., description="Letter addressee")
    introduction: str = Field(..., description="Letter introduction")
    executive_summary: str = Field(..., description="Executive summary")
    detailed_findings: List[Finding] = Field([], description="Detailed findings")
    recommendations: List[Recommendation] = Field([], description="Recommendations")
    management_responses: Optional[List[Dict[str, str]]] = Field(None, description="Management responses")
    conclusion: str = Field(..., description="Letter conclusion")
    next_steps: List[str] = Field([], description="Recommended next steps")
    signature_block: Dict[str, str] = Field({}, description="Signature information")

class AuditOpinion(BaseModel):
    company_info: CompanyInformation
    addressee: str = Field(..., description="Opinion addressee")
    opinion_type: str = Field(..., description="Type of audit opinion")
    opinion_paragraph: str = Field(..., description="Main opinion paragraph")
    basis_for_opinion: str = Field(..., description="Basis for opinion")
    key_audit_matters: List[str] = Field([], description="Key audit matters")
    responsibilities: Dict[str, str] = Field({}, description="Responsibilities section")
    independence_statement: str = Field(..., description="Independence statement")
    auditor_signature: Dict[str, str] = Field({}, description="Auditor signature block")

class ReportMetadata(BaseModel):
    report_id: str = Field(..., description="Unique report identifier")
    generation_date: str = Field(..., description="Report generation date")
    generated_by: str = Field("Nigerian Audit AI", description="Report generator")
    version: str = Field("1.0", description="Report version")
    template_version: Optional[str] = Field(None, description="Template version used")
    processing_time: float = Field(..., description="Report generation time in seconds")
    page_count: Optional[int] = Field(None, description="Number of pages")
    file_size: Optional[int] = Field(None, description="File size in bytes")

class ReportGenerationResult(BaseModel):
    report_type: ReportType
    format: ReportFormat
    metadata: ReportMetadata
    content: Union[
        FinancialAnalysisReport,
        ComplianceAssessmentReport,
        RiskAssessmentReport,
        ManagementLetter,
        AuditOpinion,
        Dict[str, Any]
    ] = Field(..., description="Report content")
    sections: List[ReportSection] = Field([], description="Report sections")
    attachments: Optional[List[Dict[str, Any]]] = Field(None, description="Report attachments")
    download_url: Optional[str] = Field(None, description="Download URL for generated file")

class ReportGenerationResponse(BaseModel):
    success: bool = Field(True, description="Whether generation was successful")
    data: Optional[ReportGenerationResult] = Field(None, description="Generation results")
    error: Optional[str] = Field(None, description="Error message if generation failed")
    timestamp: Optional[str] = Field(None, description="Generation timestamp")

class ReportTemplate(BaseModel):
    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    report_type: ReportType
    supported_formats: List[ReportFormat] = Field(..., description="Supported output formats")
    sections: List[str] = Field(..., description="Template sections")
    customizable_fields: List[str] = Field([], description="Customizable fields")
    variables: Dict[str, str] = Field({}, description="Template variables")
    styling: Optional[Dict[str, Any]] = Field(None, description="Template styling options")

class BenchmarkingData(BaseModel):
    industry: str = Field(..., description="Industry for benchmarking")
    company_size: str = Field(..., description="Company size category")
    metrics: Dict[str, float] = Field({}, description="Benchmark metrics")
    percentiles: Dict[str, Dict[str, float]] = Field({}, description="Percentile data")
    data_source: str = Field(..., description="Source of benchmark data")
    last_updated: str = Field(..., description="Last update date")

class TrendAnalysisData(BaseModel):
    metric_name: str = Field(..., description="Metric being analyzed")
    time_series: List[Dict[str, Union[str, float]]] = Field(..., description="Time series data")
    trend_direction: str = Field(..., description="Overall trend direction")
    trend_strength: str = Field(..., description="Strength of trend")
    seasonal_patterns: Optional[Dict[str, Any]] = Field(None, description="Seasonal patterns")
    forecasts: Optional[List[Dict[str, Any]]] = Field(None, description="Future forecasts")

class ComparativeAnalysis(BaseModel):
    base_period: str = Field(..., description="Base period for comparison")
    comparison_periods: List[str] = Field(..., description="Comparison periods")
    metrics_comparison: Dict[str, Dict[str, float]] = Field({}, description="Metrics comparison")
    variance_analysis: Dict[str, float] = Field({}, description="Variance analysis")
    key_changes: List[str] = Field([], description="Key changes identified")
    explanations: Dict[str, str] = Field({}, description="Explanations for changes")

class ReportDistribution(BaseModel):
    recipients: List[str] = Field(..., description="Report recipients")
    distribution_method: str = Field("email", description="Distribution method")
    access_level: str = Field("standard", description="Access level")
    expiry_date: Optional[str] = Field(None, description="Report expiry date")
    password_protected: bool = Field(False, description="Whether report is password protected")

class ReportSchedule(BaseModel):
    schedule_id: str = Field(..., description="Unique schedule identifier")
    report_type: ReportType
    frequency: str = Field(..., description="Generation frequency")
    next_generation: str = Field(..., description="Next generation date")
    recipients: List[str] = Field(..., description="Scheduled recipients")
    template_id: Optional[str] = Field(None, description="Template to use")
    active: bool = Field(True, description="Whether schedule is active")

class ReportAuditTrail(BaseModel):
    action: str = Field(..., description="Action performed")
    user: str = Field(..., description="User who performed action")
    timestamp: str = Field(..., description="Action timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional action details")
    ip_address: Optional[str] = Field(None, description="User IP address")

class ReportAccessLog(BaseModel):
    report_id: str = Field(..., description="Report identifier")
    accessed_by: str = Field(..., description="User who accessed report")
    access_timestamp: str = Field(..., description="Access timestamp")
    access_method: str = Field(..., description="Access method")
    ip_address: Optional[str] = Field(None, description="Access IP address")
    duration: Optional[float] = Field(None, description="Access duration in seconds")

# Enable forward references for self-referencing models
ReportSection.update_forward_refs()