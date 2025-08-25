from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import Dict
from contextlib import asynccontextmanager
from loguru import logger

from ..models.financial_analyzer import FinancialAnalyzer
from ..models.compliance_checker import ComplianceChecker
from ..models.risk_assessor import RiskAssessor
from ..models.account_mapper import AccountMapper
from ..models.substantive_tester import SubstantiveTester
from ..models.report_generator import ReportGenerator
from ..schemas.financial import FinancialAnalysisRequest, FinancialAnalysisResponse
from ..schemas.compliance import ComplianceCheckRequest, ComplianceCheckResponse
from ..schemas.mapping import AccountMappingRequest, AccountMappingResponse
from ..schemas.testing import SamplingRequest, SamplingResponse, WorkingPaperRequest, WorkingPaperResponse
from ..schemas.reporting import AuditReportRequest, AuditReportResponse, ManagementLetterRequest, ManagementLetterResponse
from ..config.settings import settings
from .middleware.logging import StructuredLoggingMiddleware

# Global model instances
financial_analyzer = None
compliance_checker = None
risk_assessor = None
account_mapper = None
substantive_tester = None
report_generator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global financial_analyzer, compliance_checker, risk_assessor, account_mapper, substantive_tester, report_generator
    logger.info("🚀 Starting Nigerian Audit AI API...")
    
    # Initialize models
    financial_analyzer = FinancialAnalyzer()
    compliance_checker = ComplianceChecker()
    risk_assessor = RiskAssessor()
    account_mapper = AccountMapper()
    substantive_tester = SubstantiveTester()
    report_generator = ReportGenerator()
    
    logger.info("✅ Models loaded successfully")
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Nigerian Audit AI API...")

# Create FastAPI app
app = FastAPI(
    title="Nigerian Audit AI",
    description="AI-powered audit system for Nigerian financial regulations",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add structured logging middleware
app.add_middleware(StructuredLoggingMiddleware)

# Security
security = HTTPBearer()

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key"""
    if credentials.credentials != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

@app.get("/")
async def root():
    return {
        "message": "Nigerian Audit AI API",
        "version": settings.VERSION,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": {
            "financial_analyzer": financial_analyzer is not None,
            "compliance_checker": compliance_checker is not None,
            "risk_assessor": risk_assessor is not None
        }
    }

@app.post("/api/v1/analyze/financial", response_model=FinancialAnalysisResponse)
async def analyze_financial_data(
    request: FinancialAnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """Analyze financial data and trial balance"""
    try:
        result = financial_analyzer.analyze_financial_data(
            trial_balance=request.trial_balance,
            company_info=request.company_info
        )
        
        return FinancialAnalysisResponse(
            success=True,
            data=result
        )
        
    except Exception as e:
        logger.error(f"Financial analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/compliance/check", response_model=ComplianceCheckResponse)
async def check_compliance(
    request: ComplianceCheckRequest,
    api_key: str = Depends(verify_api_key)
):
    """Check compliance with Nigerian regulations"""
    try:
        result = compliance_checker.check_compliance(
            company_data=request.company_data,
            financial_data=request.financial_data,
            regulations=request.regulations
        )
        
        return ComplianceCheckResponse(
            success=True,
            data=result
        )
        
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/risk/assess")
async def assess_risk(
    financial_data: Dict,
    company_info: Dict,
    api_key: str = Depends(verify_api_key)
):
    """Assess financial and operational risks"""
    try:
        result = risk_assessor.assess_risk(
            financial_data=financial_data,
            company_info=company_info
        )
        
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Risk assessment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/mapping/accounts", response_model=AccountMappingResponse)
async def map_accounts_endpoint(
    request: AccountMappingRequest,
    api_key: str = Depends(verify_api_key)
):
    """Map GL accounts and build a lead schedule"""
    try:
        mapped_accounts = account_mapper.map_accounts(request.trial_balance)
        lead_schedule = account_mapper.build_lead_schedule(mapped_accounts)
        
        return AccountMappingResponse(
            success=True,
            mapped_accounts=mapped_accounts,
            lead_schedule=lead_schedule.to_dict(orient="records")
        )
        
    except Exception as e:
        logger.error(f"Account mapping error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/testing/sampling", response_model=SamplingResponse)
async def suggest_sampling_endpoint(
    request: SamplingRequest,
    api_key: str = Depends(verify_api_key)
):
    """Suggest audit samples based on materiality and risk"""
    try:
        suggestions = substantive_tester.suggest_sampling(
            trial_balance=request.trial_balance,
            materiality=request.materiality,
            risk_level=request.risk_level
        )
        return SamplingResponse(success=True, suggestions=suggestions)
    except Exception as e:
        logger.error(f"Sampling suggestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/testing/working-paper", response_model=WorkingPaperResponse)
async def generate_working_paper_endpoint(
    request: WorkingPaperRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate a working paper for a specific account"""
    try:
        working_paper = substantive_tester.generate_working_paper(
            account_name=request.account_name,
            transactions=request.transactions
        )
        return WorkingPaperResponse(
            success=True,
            working_paper=working_paper.to_dict(orient="records"),
            title=working_paper.attrs.get("title", "")
        )
    except Exception as e:
        logger.error(f"Working paper generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/reporting/audit-report", response_model=AuditReportResponse)
async def generate_audit_report_endpoint(
    request: AuditReportRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate a draft audit report"""
    try:
        report = report_generator.generate_audit_report(
            company_name=request.company_name,
            opinion=request.opinion,
            findings=request.findings
        )
        return AuditReportResponse(success=True, report=report)
    except Exception as e:
        logger.error(f"Audit report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/reporting/management-letter", response_model=ManagementLetterResponse)
async def generate_management_letter_endpoint(
    request: ManagementLetterRequest,
    api_key: str = Depends(verify_api_key)
):
    """Generate a draft management letter"""
    try:
        letter = report_generator.generate_management_letter(
            company_name=request.company_name,
            deficiencies=request.deficiencies
        )
        return ManagementLetterResponse(success=True, letter=letter)
    except Exception as e:
        logger.error(f"Management letter generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/validate/nigerian")
async def validate_nigerian_data(
    data: Dict,
    validation_type: str,
    api_key: str = Depends(verify_api_key)
):
    """Validate Nigerian-specific data (TIN, CAC, etc.)"""
    try:
        from ..utils.validators import NigerianValidator
        
        validator = NigerianValidator()
        result = validator.validate(data, validation_type)
        
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
