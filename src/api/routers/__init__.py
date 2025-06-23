"""
API Routers for Nigerian Audit AI

This module contains all the API route definitions organized by functionality.
"""

from fastapi import APIRouter
from .financial import router as financial_router
from .compliance import router as compliance_router
from .risk import router as risk_router
from .validation import router as validation_router
from .documents import router as documents_router
from .reports import router as reports_router

# Main API router
api_router = APIRouter(prefix="/api/v1")

# Include all sub-routers
api_router.include_router(
    financial_router,
    prefix="/analyze",
    tags=["Financial Analysis"],
)

api_router.include_router(
    compliance_router,
    prefix="/compliance",
    tags=["Compliance Checking"],
)

api_router.include_router(
    risk_router,
    prefix="/risk",
    tags=["Risk Assessment"],
)

api_router.include_router(
    validation_router,
    prefix="/validate",
    tags=["Data Validation"],
)

api_router.include_router(
    documents_router,
    prefix="/documents",
    tags=["Document Processing"],
)

api_router.include_router(
    reports_router,
    prefix="/reports",
    tags=["Report Generation"],
)

__all__ = ["api_router"]