from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional
import logging
from datetime import datetime

from ...schemas.compliance import (
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    ComplianceRegulation
)
from ...models.compliance_checker import ComplianceChecker
from ...api.dependencies import get_compliance_checker, verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/check", response_model=ComplianceCheckResponse)
async def check_compliance(
    request: ComplianceCheckRequest,
    background_tasks: BackgroundTasks,
    checker: ComplianceChecker = Depends(get_compliance_checker),
    api_key: str = Depends(verify_api_key)
):
    """
    Check compliance against Nigerian regulations
    
    Supports checking against:
    - FRC (Financial Reporting Council)
    - FIRS (Federal Inland Revenue Service)  
    - CAMA (Companies and Allied Matters Act)
    - CBN (Central Bank of Nigeria)
    """
    try:
        logger.info(f"Processing compliance check for {len(request.regulations)} regulations")
        
        # Perform compliance check
        result = checker.check_compliance(
            company_data=request.company_data.dict(),
            financial_data=request.financial_data.dict(),
            regulations=request.regulations
        )
        
        # Add background task for logging
        background_tasks.add_task(
            log_compliance_check,
            company_data=request.company_data,
            regulations=request.regulations,
            api_key=api_key
        )
        
        return ComplianceCheckResponse(
            success=True,
            data=result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Compliance check failed: {str(e)}"
        )

@router.post("/frc")
async def check_frc_compliance(
    company_data: Dict,
    financial_data: Dict,
    checker: ComplianceChecker = Depends(get_compliance_checker),
    api_key: str = Depends(verify_api_key)
):
    """Check Financial Reporting Council (FRC) compliance"""
    
    try:
        result = checker._check_frc_compliance(company_data, financial_data)
        
        return {
            "success": True,
            "data": result,
            "regulation": "FRC",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"FRC compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/firs")
async def check_firs_compliance(
    company_data: Dict,
    financial_data: Dict,
    checker: ComplianceChecker = Depends(get_compliance_checker),
    api_key: str = Depends(verify_api_key)
):
    """Check Federal Inland Revenue Service (FIRS) compliance"""
    
    try:
        result = checker._check_firs_compliance(company_data, financial_data)
        
        return {
            "success": True,
            "data": result,
            "regulation": "FIRS",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"FIRS compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cama")
async def check_cama_compliance(
    company_data: Dict,
    financial_data: Dict,
    checker: ComplianceChecker = Depends(get_compliance_checker),
    api_key: str = Depends(verify_api_key)
):
    """Check Companies and Allied Matters Act (CAMA) compliance"""
    
    try:
        result = checker._check_cama_compliance(company_data, financial_data)
        
        return {
            "success": True,
            "data": result,
            "regulation": "CAMA",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"CAMA compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cbn")
async def check_cbn_compliance(
    company_data: Dict,
    financial_data: Dict,
    checker: ComplianceChecker = Depends(get_compliance_checker),
    api_key: str = Depends(verify_api_key)
):
    """Check Central Bank of Nigeria (CBN) compliance (for banks)"""
    
    try:
        result = checker._check_cbn_compliance(company_data, financial_data)
        
        return {
            "success": True,
            "data": result,
            "regulation": "CBN",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"CBN compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regulations")
async def get_supported_regulations():
    """Get list of supported Nigerian regulations"""
    
    regulations = [
        {
            "code": "FRC",
            "name": "Financial Reporting Council",
            "description": "Financial reporting standards and corporate governance",
            "applicability": "Public companies and significant private companies",
            "key_requirements": [
                "Financial statement filing",
                "IFRS compliance",
                "Corporate governance",
                "Audit quality"
            ]
        },
        {
            "code": "FIRS",
            "name": "Federal Inland Revenue Service",
            "description": "Tax administration and collection",
            "applicability": "All business entities",
            "key_requirements": [
                "TIN registration",
                "VAT registration",
                "Tax filing",
                "Withholding tax compliance"
            ]
        },
        {
            "code": "CAMA",
            "name": "Companies and Allied Matters Act",
            "description": "Company registration and regulation",
            "applicability": "All incorporated companies",
            "key_requirements": [
                "CAC registration",
                "Annual returns",
                "Corporate governance",
                "Director obligations"
            ]
        },
        {
            "code": "CBN",
            "name": "Central Bank of Nigeria",
            "description": "Banking regulation and monetary policy",
            "applicability": "Banks and financial institutions",
            "key_requirements": [
                "Capital adequacy",
                "Liquidity ratios",
                "Prudential guidelines",
                "Risk management"
            ]
        }
    ]
    
    return {
        "success": True,
        "data": {
            "regulations": regulations,
            "total_count": len(regulations)
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/requirements/{regulation}")
async def get_regulation_requirements(
    regulation: ComplianceRegulation,
    company_type: Optional[str] = None,
    company_size: Optional[str] = None
):
    """Get detailed requirements for a specific regulation"""
    
    try:
        requirements_map = {
            "FRC": {
                "filing_requirements": [
                    "Annual financial statements within 90 days",
                    "Directors' report",
                    "Auditor's report",
                    "Corporate governance statement"
                ],
                "compliance_thresholds": {
                    "public_companies": "All public companies",
                    "private_companies": "Revenue > ₦500M or Assets > ₦1B"
                },
                "penalties": "₦500,000 - ₦5,000,000"
            },
            "FIRS": {
                "filing_requirements": [
                    "Annual tax returns within 6 months",
                    "Monthly VAT returns",
                    "WHT remittance within 21 days",
                    "PAYE remittance within 10 days"
                ],
                "registration_requirements": [
                    "TIN registration for all entities",
                    "VAT registration if turnover > ₦25M"
                ],
                "penalties": "₦25,000 + 10% of tax due"
            },
            "CAMA": {
                "filing_requirements": [
                    "Annual returns within 42 days of AGM",
                    "Notice of change of directors within 15 days",
                    "Notice of change of address within 15 days"
                ],
                "corporate_governance": [
                    "Board meetings as per Articles",
                    "Maintain statutory registers",
                    "File special resolutions"
                ],
                "penalties": "₦10,000 - ₦200,000"
            },
            "CBN": {
                "prudential_requirements": [
                    "Capital adequacy ratio ≥ 15%",
                    "Liquidity ratio ≥ 30%",
                    "Credit risk management",
                    "Operational risk controls"
                ],
                "reporting_requirements": [
                    "Monthly prudential returns",
                    "Quarterly financial statements",
                    "Annual compliance certificate"
                ],
                "applicability": "Banks and financial institutions only"
            }
        }
        
        regulation_data = requirements_map.get(regulation)
        if not regulation_data:
            raise HTTPException(status_code=404, detail="Regulation not found")
        
        return {
            "success": True,
            "data": {
                "regulation": regulation,
                "requirements": regulation_data,
                "company_type": company_type,
                "company_size": company_size
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Requirements lookup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def compliance_health_check():
    """Health check for compliance service"""
    
    return {
        "status": "healthy",
        "service": "compliance_checking",
        "timestamp": datetime.utcnow().isoformat(),
        "supported_regulations": ["FRC", "FIRS", "CAMA", "CBN"],
        "features": [
            "multi_regulation_checking",
            "violation_detection",
            "penalty_assessment",
            "recommendation_generation"
        ]
    }

async def log_compliance_check(company_data: Dict, regulations: List[str], api_key: str):
    """Background task to log compliance checks"""
    
    try:
        log_data = {
            "request_type": "compliance_check",
            "timestamp": datetime.utcnow().isoformat(),
            "api_key_hash": hash(api_key),
            "regulations_checked": regulations,
            "company_type": company_data.get("business_type"),
            "is_public": company_data.get("is_public", False)
        }
        
        logger.info(f"Compliance check logged: {log_data}")
        
    except Exception as e:
        logger.error(f"Failed to log compliance check: {e}")