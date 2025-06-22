from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import Dict, List, Optional
import logging
from contextlib import asynccontextmanager

from ..models.financial_analyzer import FinancialAnalyzer
from ..models.compliance_checker import ComplianceChecker
from ..models.risk_assessor import RiskAssessor
from ..schemas.financial import FinancialAnalysisRequest, FinancialAnalysisResponse
from ..schemas.compliance import ComplianceCheckRequest, ComplianceCheckResponse
from ..config.settings import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instances
financial_analyzer = None
compliance_checker = None
risk_assessor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global financial_analyzer, compliance_checker, risk_assessor
    logger.info("🚀 Starting Nigerian Audit AI API...")
    
    # Initialize models
    financial_analyzer = FinancialAnalyzer()
    compliance_checker = ComplianceChecker()
    risk_assessor = RiskAssessor()
    
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