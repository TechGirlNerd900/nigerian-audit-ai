from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional
import logging
from datetime import datetime

from ...schemas.financial import (
    FinancialAnalysisRequest, 
    FinancialAnalysisResponse,
    FinancialAnalysisData
)
from ...models.financial_analyzer import FinancialAnalyzer
from ...api.dependencies import get_financial_analyzer, verify_api_key

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/financial", response_model=FinancialAnalysisResponse)
async def analyze_financial_data(
    request: FinancialAnalysisRequest,
    background_tasks: BackgroundTasks,
    analyzer: FinancialAnalyzer = Depends(get_financial_analyzer),
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze financial data and trial balance
    
    Performs comprehensive financial analysis including:
    - Account classification according to Nigerian standards
    - Financial ratio calculations
    - Risk assessment
    - Compliance checking
    """
    try:
        logger.info(f"Processing financial analysis request with {len(request.trial_balance)} accounts")
        
        # Perform analysis
        result = analyzer.analyze_financial_data(
            trial_balance=request.trial_balance,
            company_info=request.company_info.dict() if request.company_info else None
        )
        
        # Add background task for logging
        background_tasks.add_task(
            log_analysis_request,
            request_type="financial_analysis",
            company_info=request.company_info,
            api_key=api_key
        )
        
        return FinancialAnalysisResponse(
            success=True,
            data=FinancialAnalysisData(**result),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Financial analysis error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Financial analysis failed: {str(e)}"
        )

@router.post("/ratios")
async def calculate_financial_ratios(
    trial_balance: Dict[str, float],
    company_type: str = "general",
    analyzer: FinancialAnalyzer = Depends(get_financial_analyzer),
    api_key: str = Depends(verify_api_key)
):
    """Calculate financial ratios from trial balance"""
    
    try:
        # Preprocess trial balance
        classification = analyzer.preprocess_trial_balance(trial_balance)
        
        # Calculate ratios
        ratios = analyzer.calculate_financial_ratios(classification)
        
        return {
            "success": True,
            "data": {
                "ratios": ratios,
                "classification_summary": {
                    "total_assets": sum(classification['current_assets'].values()) + 
                                  sum(classification['non_current_assets'].values()),
                    "total_liabilities": sum(classification['current_liabilities'].values()) + 
                                       sum(classification['non_current_liabilities'].values()),
                    "total_equity": sum(classification['equity'].values())
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Ratio calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/classification")
async def classify_accounts(
    trial_balance: Dict[str, float],
    analyzer: FinancialAnalyzer = Depends(get_financial_analyzer),
    api_key: str = Depends(verify_api_key)
):
    """Classify trial balance accounts according to Nigerian standards"""
    
    try:
        classification = analyzer.preprocess_trial_balance(trial_balance)
        formatted_classification = analyzer._format_amounts(classification)
        
        return {
            "success": True,
            "data": {
                "classification": formatted_classification,
                "account_count": sum(len(accounts) for accounts in classification.values()),
                "categories": list(classification.keys())
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Account classification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/benchmark")
async def compare_to_benchmark(
    ratios: Dict[str, float],
    industry: str = "general",
    company_size: str = "medium",
    analyzer: FinancialAnalyzer = Depends(get_financial_analyzer),
    api_key: str = Depends(verify_api_key)
):
    """Compare financial ratios to Nigerian industry benchmarks"""
    
    try:
        # Get benchmarks
        benchmarks = analyzer.nigerian_ratios.get_benchmarks(industry)
        
        # Compare ratios
        comparison = {}
        for ratio_name, ratio_value in ratios.items():
            if ratio_name in benchmarks:
                benchmark = benchmarks[ratio_name]
                comparison[ratio_name] = {
                    "value": ratio_value,
                    "benchmark": benchmark,
                    "performance": analyzer._score_ratio(ratio_name, ratio_value, benchmark),
                    "status": "above_benchmark" if ratio_value > benchmark.get('target', 0) else "below_benchmark"
                }
        
        return {
            "success": True,
            "data": {
                "comparison": comparison,
                "industry": industry,
                "company_size": company_size,
                "benchmarks_used": benchmarks
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Benchmark comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def financial_health_check():
    """Health check for financial analysis service"""
    
    return {
        "status": "healthy",
        "service": "financial_analysis",
        "timestamp": datetime.utcnow().isoformat(),
        "features": [
            "account_classification",
            "ratio_calculation", 
            "risk_assessment",
            "benchmark_comparison"
        ]
    }

async def log_analysis_request(request_type: str, company_info: Optional[Dict], api_key: str):
    """Background task to log analysis requests"""
    
    try:
        log_data = {
            "request_type": request_type,
            "timestamp": datetime.utcnow().isoformat(),
            "api_key_hash": hash(api_key),  # Don't store actual API key
            "company_type": company_info.get("type") if company_info else None,
            "company_size": company_info.get("size") if company_info else None
        }
        
        logger.info(f"Analysis request logged: {log_data}")
        
    except Exception as e:
        logger.error(f"Failed to log analysis request: {e}")