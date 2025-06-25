# src/api/dependencies.py
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging
from ..config.settings import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify API key authentication"""
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if credentials.credentials != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials

async def get_current_user(api_key: str = Depends(verify_api_key)) -> dict:
    """Get current user from API key (placeholder implementation)"""
    
    # In a real implementation, this would look up user from database
    return {
        "user_id": "api_user",
        "api_key": api_key,
        "permissions": ["read", "write"],
        "rate_limit": 1000
    }

def require_permissions(required_permissions: list):
    """Dependency to require specific permissions"""
    
    async def permission_checker(user: dict = Depends(get_current_user)):
        user_permissions = user.get("permissions", [])
        
        for permission in required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission: {permission}"
                )
        
        return user
    
    return permission_checker

---

# src/scrapers/cac_scraper.py
import asyncio
import logging
from typing import Dict, List
from datetime import datetime
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class CACScraper(BaseScraper):
    """Scraper for Corporate Affairs Commission (CAC) data"""
    
    def __init__(self):
        super().__init__(delay=5)
        self.base_url = "https://pre.cac.gov.ng"
    
    async def collect_data(self) -> Dict:
        """Collect CAC registration and company data"""
        
        logger.info("Starting CAC data collection...")
        
        try:
            # Collect different types of CAC data
            registration_data = await self._collect_registration_requirements()
            forms_data = await self._collect_cac_forms()
            fees_data = await self._collect_fee_schedule()
            
            collected_data = {
                'source': 'CAC Nigeria',
                'collection_date': datetime.now().isoformat(),
                'registration_requirements': registration_data,
                'forms': forms_data,
                'fee_schedule': fees_data,
                'base_url': self.base_url
            }
            
            # Save data
            self.save_data(collected_data, f'cac_data_{datetime.now().strftime("%Y%m%d")}.json')
            
            return collected_data
            
        except Exception as e:
            logger.error(f"CAC data collection failed: {e}")
            return {'error': str(e)}
    
    async def _collect_registration_requirements(self) -> List[Dict]:
        """Collect company registration requirements"""
        
        requirements = [
            {
                'entity_type': 'Private Company Limited by Shares',
                'code': 'RC',
                'minimum_shareholders': 2,
                'maximum_shareholders': 50,
                'minimum_share_capital': 100000,  # ₦100,000
                'documents_required': [
                    'Memorandum and Articles of Association',
                    'Notice of Address of Registered Office',
                    'Statement of Share Capital and Return of Allotment',
                    'List of First Directors',
                    'Declaration of Compliance'
                ],
                'processing_time': '24-48 hours',
                'annual_return_required': True
            },
            {
                'entity_type': 'Public Company Limited by Shares',
                'code': 'PLC',
                'minimum_shareholders': 7,
                'maximum_shareholders': None,
                'minimum_share_capital': 2000000,  # ₦2,000,000
                'documents_required': [
                    'Memorandum and Articles of Association',
                    'Notice of Address of Registered Office',
                    'Statement of Share Capital',
                    'List of First Directors',
                    'Declaration of Compliance',
                    'SEC Approval (if applicable)'
                ],
                'processing_time': '3-5 days',
                'annual_return_required': True
            },
            {
                'entity_type': 'Business Name',
                'code': 'BN',
                'minimum_shareholders': 1,
                'maximum_shareholders': None,
                'minimum_share_capital': 0,
                'documents_required': [
                    'Business Name Registration Form',
                    'Proprietor Identification',
                    'Business Address Proof'
                ],
                'processing_time': '24 hours',
                'annual_return_required': False
            }
        ]
        
        logger.info(f"Collected {len(requirements)} registration requirements")
        return requirements
    
    async def _collect_cac_forms(self) -> List[Dict]:
        """Collect information about CAC forms"""
        
        forms = [
            {
                'form_code': 'CAC 1.1',
                'form_name': 'Application for Reservation of Name',
                'purpose': 'Reserve company/business name',
                'fee': 500,
                'validity': '60 days'
            },
            {
                'form_code': 'CAC 2',
                'form_name': 'Statement of Share Capital and Return of Allotment',
                'purpose': 'Declare share capital structure',
                'fee': 'Based on share capital',
                'validity': 'Permanent'
            },
            {
                'form_code': 'CAC 3',
                'form_name': 'Notice of Registered Address',
                'purpose': 'Register company address',
                'fee': 0,
                'validity': 'Until changed'
            },
            {
                'form_code': 'CAC 7',
                'form_name': 'Particulars of Directors',
                'purpose': 'Register company directors',
                'fee': 0,
                'validity': 'Until changed'
            },
            {
                'form_code': 'CAC 8',
                'form_name': 'Annual Return',
                'purpose': 'File annual company information',
                'fee': 'Based on company type',
                'validity': 'Annual'
            }
        ]
        
        logger.info(f"Collected {len(forms)} CAC forms")
        return forms
    
    async def _collect_fee_schedule(self) -> Dict:
        """Collect CAC fee schedule"""
        
        fees = {
            'registration_fees': {
                'private_company': {
                    'up_to_1m': 10000,
                    '1m_to_10m': 20000,
                    '10m_to_100m': 50000,
                    'above_100m': 100000
                },
                'public_company': {
                    'up_to_1m': 20000,
                    '1m_to_10m': 40000,
                    '10m_to_100m': 100000,
                    'above_100m': 200000
                },
                'business_name': 10000
            },
            'annual_return_fees': {
                'private_company': 5000,
                'public_company': 10000,
                'business_name': 0
            },
            'change_of_name': 15000,
            'increase_in_share_capital': 'Based on increase amount',
            'certified_true_copy': 2000,
            'status_report': 25000
        }
        
        logger.info("Collected CAC fee schedule")
        return fees

---

# src/api/routers/financial.py
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional
import logging
from ...models.financial_analyzer import FinancialAnalyzer
from ...schemas.financial import (
    FinancialAnalysisRequest, 
    FinancialAnalysisResponse,
    FinancialAnalysisData
)
from ...api.dependencies import get_current_user, verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/financial", tags=["Financial Analysis"])

# Global analyzer instance
analyzer = FinancialAnalyzer()

@router.post("/analyze", response_model=FinancialAnalysisResponse)
async def analyze_financial_data(
    request: FinancialAnalysisRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze financial data and trial balance
    
    Performs comprehensive financial analysis including:
    - Account classification according to Nigerian standards
    - Financial ratio calculations
    - Risk assessment using Nigerian benchmarks
    - Compliance flag identification
    """
    try:
        logger.info(f"Processing financial analysis for {len(request.trial_balance)} accounts")
        
        # Perform analysis
        result = analyzer.analyze_financial_data(
            trial_balance=request.trial_balance,
            company_info=request.company_info.dict() if request.company_info else None
        )
        
        # Add background task for audit logging
        background_tasks.add_task(
            log_analysis_request,
            "financial_analysis",
            request.trial_balance,
            result
        )
        
        return FinancialAnalysisResponse(
            success=True,
            data=FinancialAnalysisData(**result),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except ValueError as e:
        logger.error(f"Validation error in financial analysis: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Financial analysis error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")

@router.post("/ratios/calculate")
async def calculate_ratios(
    trial_balance: Dict[str, float],
    company_type: str = "general",
    api_key: str = Depends(verify_api_key)
):
    """Calculate financial ratios from trial balance"""
    try:
        # Classify accounts first
        classification = analyzer.preprocess_trial_balance(trial_balance)
        
        # Calculate ratios
        ratios = analyzer.calculate_financial_ratios(classification)
        
        return {
            "success": True,
            "ratios": ratios,
            "company_type": company_type,
            "calculation_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Ratio calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/classify")
async def classify_accounts(
    accounts: Dict[str, float],
    api_key: str = Depends(verify_api_key)
):
    """Classify chart of accounts according to Nigerian standards"""
    try:
        classification = analyzer.preprocess_trial_balance(accounts)
        
        return {
            "success": True,
            "classification": classification,
            "total_accounts": len(accounts),
            "classification_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Account classification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/benchmarks/{industry}")
async def get_industry_benchmarks(
    industry: str,
    api_key: str = Depends(verify_api_key)
):
    """Get Nigerian industry financial benchmarks"""
    try:
        benchmarks = analyzer.nigerian_ratios.get_benchmarks(industry)
        
        return {
            "success": True,
            "industry": industry,
            "benchmarks": benchmarks,
            "currency": "NGN"
        }
        
    except Exception as e:
        logger.error(f"Benchmark retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def log_analysis_request(analysis_type: str, input_data: Dict, result: Dict):
    """Background task to log analysis requests"""
    # This would log to database or audit system
    logger.info(f"Analysis completed: {analysis_type}")

---

# src/api/routers/compliance.py
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional
import logging
from ...models.compliance_checker import ComplianceChecker
from ...schemas.compliance import (
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    ComplianceCheckData
)
from ...api.dependencies import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/compliance", tags=["Compliance Checking"])

# Global compliance checker instance
compliance_checker = ComplianceChecker()

@router.post("/check", response_model=ComplianceCheckResponse)
async def check_compliance(
    request: ComplianceCheckRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Check compliance with Nigerian regulations
    
    Supports checking against:
    - FRC (Financial Reporting Council)
    - FIRS (Federal Inland Revenue Service)  
    - CAMA (Companies and Allied Matters Act)
    - CBN (Central Bank of Nigeria)
    - SEC (Securities and Exchange Commission)
    """
    try:
        logger.info(f"Processing compliance check for {request.regulations}")
        
        # Perform compliance check
        result = compliance_checker.check_compliance(
            company_data=request.company_data.dict(),
            financial_data=request.financial_data.dict(),
            regulations=request.regulations
        )
        
        # Add background task for logging
        background_tasks.add_task(
            log_compliance_check,
            request.company_data.cac_number,
            request.regulations,
            result
        )
        
        return ComplianceCheckResponse(
            success=True,
            data=ComplianceCheckData(**result),
            timestamp=datetime.utcnow().isoformat()
        )
        
    except ValueError as e:
        logger.error(f"Validation error in compliance check: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Compliance check error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during compliance check")

@router.post("/frc/check")
async def check_frc_compliance(
    company_data: Dict,
    financial_data: Dict,
    api_key: str = Depends(verify_api_key)
):
    """Check specific FRC compliance requirements"""
    try:
        result = compliance_checker._check_frc_compliance(company_data, financial_data)
        
        return {
            "success": True,
            "regulation": "FRC",
            "result": result,
            "check_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"FRC compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/firs/check")
async def check_firs_compliance(
    company_data: Dict,
    financial_data: Dict,
    api_key: str = Depends(verify_api_key)
):
    """Check specific FIRS tax compliance requirements"""
    try:
        result = compliance_checker._check_firs_compliance(company_data, financial_data)
        
        return {
            "success": True,
            "regulation": "FIRS", 
            "result": result,
            "check_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"FIRS compliance check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regulations")
async def get_supported_regulations(api_key: str = Depends(verify_api_key)):
    """Get list of supported Nigerian regulations"""
    
    regulations = [
        {
            "code": "FRC",
            "name": "Financial Reporting Council of Nigeria",
            "description": "Financial reporting and corporate governance requirements",
            "applicability": "Public companies and significant private companies"
        },
        {
            "code": "FIRS", 
            "name": "Federal Inland Revenue Service",
            "description": "Tax compliance and filing requirements",
            "applicability": "All business entities"
        },
        {
            "code": "CAMA",
            "name": "Companies and Allied Matters Act 2020",
            "description": "Company registration and corporate compliance",
            "applicability": "All incorporated entities"
        },
        {
            "code": "CBN",
            "name": "Central Bank of Nigeria",
            "description": "Banking and financial institution regulations",
            "applicability": "Banks and financial institutions"
        }
    ]
    
    return {
        "success": True,
        "regulations": regulations,
        "total_count": len(regulations)
    }

async def log_compliance_check(cac_number: str, regulations: List[str], result: Dict):
    """Background task to log compliance checks"""
    logger.info(f"Compliance check completed for {cac_number}: {regulations}")

---

# src/api/routers/validation.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
import logging
from ...utils.validators import NigerianValidator
from ...utils.currency import format_ngn, validate_ngn_amount
from ...schemas.responses import NigerianValidationResponse
from ...api.dependencies import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/validate", tags=["Nigerian Data Validation"])

# Global validator instance
validator = NigerianValidator()

@router.post("/cac", response_model=NigerianValidationResponse)
async def validate_cac_number(
    cac_number: str,
    api_key: str = Depends(verify_api_key)
):
    """Validate Nigerian CAC registration number"""
    try:
        result = validator.validate_cac_number(cac_number)
        
        return NigerianValidationResponse(
            success=True,
            validation_type="CAC Registration Number",
            valid=result['valid'],
            format_valid=result['format_valid'],
            api_verified=result['api_verified'],
            details=result
        )
        
    except Exception as e:
        logger.error(f"CAC validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tin")
async def validate_tin_number(
    tin_number: str,
    api_key: str = Depends(verify_api_key)
):
    """Validate Nigerian Tax Identification Number (TIN)"""
    try:
        result = validator.validate_tin_number(tin_number)
        
        return NigerianValidationResponse(
            success=True,
            validation_type="Tax Identification Number",
            valid=result['valid'],
            format_valid=result['format_valid'],
            api_verified=result['api_verified'],
            details=result
        )
        
    except Exception as e:
        logger.error(f"TIN validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/phone")
async def validate_phone_number(
    phone_number: str,
    api_key: str = Depends(verify_api_key)
):
    """Validate Nigerian phone number"""
    try:
        result = validator.validate_phone_number(phone_number)
        
        return {
            "success": True,
            "validation_type": "Nigerian Phone Number",
            "valid": result['valid'],
            "format_valid": result['format_valid'],
            "network": result['network'],
            "formatted": result['formatted'],
            "details": result
        }
        
    except Exception as e:
        logger.error(f"Phone validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bank-account")
async def validate_bank_account(
    account_number: str,
    bank_code: str,
    api_key: str = Depends(verify_api_key)
):
    """Validate Nigerian bank account number"""
    try:
        result = validator.validate_bank_account(account_number, bank_code)
        
        return {
            "success": True,
            "validation_type": "Nigerian Bank Account",
            "valid": result['valid'],
            "format_valid": result['format_valid'],
            "account_name": result['account_name'],
            "details": result
        }
        
    except Exception as e:
        logger.error(f"Bank account validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/currency")
async def validate_currency_amount(
    amount: str,
    api_key: str = Depends(verify_api_key)
):
    """Validate and format Nigerian Naira amount"""
    try:
        is_valid = validate_ngn_amount(amount)
        formatted = format_ngn(amount) if is_valid else None
        
        return {
            "success": True,
            "validation_type": "Nigerian Naira Amount",
            "valid": is_valid,
            "original_amount": amount,
            "formatted_amount": formatted,
            "currency": "NGN"
        }
        
    except Exception as e:
        logger.error(f"Currency validation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/banks")
async def get_nigerian_banks(api_key: str = Depends(verify_api_key)):
    """Get list of Nigerian banks with codes"""
    
    banks = [
        {"name": "Access Bank Plc", "code": "044", "sort_code": "044150149"},
        {"name": "Citibank Nigeria Limited", "code": "023", "sort_code": "023150005"},
        {"name": "Ecobank Nigeria Plc", "code": "050", "sort_code": "050150010"},
        {"name": "Fidelity Bank Plc", "code": "070", "sort_code": "070150003"},
        {"name": "First Bank of Nigeria Limited", "code": "011", "sort_code": "011151003"},
        {"name": "First City Monument Bank Plc", "code": "214", "sort_code": "214150018"},
        {"name": "Guaranty Trust Bank Plc", "code": "058", "sort_code": "058152036"},
        {"name": "Heritage Banking Company Ltd", "code": "030", "sort_code": "030159992"},
        {"name": "Jaiz Bank Plc", "code": "301", "sort_code": "301080020"},
        {"name": "Keystone Bank Limited", "code": "082", "sort_code": "082150017"},
        {"name": "Polaris Bank Plc", "code": "076", "sort_code": "076151006"},
        {"name": "Providus Bank", "code": "101", "sort_code": "101234567"},
        {"name": "Stanbic IBTC Bank Plc", "code": "221", "sort_code": "221159522"},
        {"name": "Standard Chartered Bank Nigeria Ltd", "code": "068", "sort_code": "068150015"},
        {"name": "Sterling Bank Plc", "code": "232", "sort_code": "232150016"},
        {"name": "Union Bank of Nigeria Plc", "code": "032", "sort_code": "032080474"},
        {"name": "United Bank For Africa Plc", "code": "033", "sort_code": "033153513"},
        {"name": "Unity Bank Plc", "code": "215", "sort_code": "215154097"},
        {"name": "Wema Bank Plc", "code": "035", "sort_code": "035150103"},
        {"name": "Zenith Bank Plc", "code": "057", "sort_code": "057150013"}
    ]
    
    return {
        "success": True,
        "banks": banks,
        "total_count": len(banks),
        "currency": "NGN"
    }

---

# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "storage.googleapis.com",
    "bigquery.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "documentai.googleapis.com",
    "secretmanager.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
}

# Storage bucket for data and models
resource "google_storage_bucket" "audit_ai_bucket" {
  name          = "${var.project_id}-nigerian-audit-ai"
  location      = var.region
  force_destroy = true
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Delete"
    }
  }
}

# BigQuery dataset
resource "google_bigquery_dataset" "audit_dataset" {
  dataset_id    = "nigerian_audit_ai"
  friendly_name = "Nigerian Audit AI Dataset"
  description   = "Dataset for Nigerian audit AI training and analytics"
  location      = var.region
  
  default_table_expiration_ms = 86400000  # 1 day
  
  access {
    role          = "OWNER"
    user_by_email = var.admin_email
  }
}

# Cloud Run service
resource "google_cloud_run_service" "audit_ai_api" {
  name     = "nigerian-audit-ai-api"
  location = var.region
  
  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/nigerian-audit-ai:latest"
        
        ports {
          container_port = 8080
        }
        
        env {
          name  = "GOOGLE_CLOUD_PROJECT_ID"
          value = var.project_id
        }
        
        env {
          name  = "GCP_REGION"
          value = var.region
        }
        
        env {
          name  = "GCS_BUCKET"
          value = google_storage_bucket.audit_ai_bucket.name
        }
        
        resources {
          limits = {
            cpu    = "2"
            memory = "4Gi"
          }
          requests = {
            cpu    = "1"
            memory = "2Gi"
          }
        }
      }
      
      container_concurrency = 100
      timeout_seconds      = 300
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/cpu-throttling" = "false"
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Run IAM
resource "google_cloud_run_service_iam_binding" "public_access" {
  location = google_cloud_run_service.audit_ai_api.location
  project  = google_cloud_run_service.audit_ai_api.project
  service  = google_cloud_run_service.audit_ai_api.name
  role     = "roles/run.invoker"
  
  members = [
    "allUsers",
  ]
}

# Service account for the application
resource "google_service_account" "audit_ai_sa" {
  account_id   = "nigerian-audit-ai"
  display_name = "Nigerian Audit AI Service Account"
  description  = "Service account for Nigerian Audit AI application"
}

# IAM roles for service account
resource "google_project_iam_member" "audit_ai_permissions" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.admin", 
    "roles/bigquery.admin",
    "roles/documentai.admin"
  ])
  
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.audit_ai_sa.email}"
}

# Secret for API key
resource "google_secret_manager_secret" "api_key" {
  secret_id = "nigerian-audit-ai-api-key"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "api_key_version" {
  secret      = google_secret_manager_secret.api_key.id
  secret_data = var.api_key
}

# Monitoring dashboard
resource "google_monitoring_dashboard" "audit_ai_dashboard" {
  dashboard_json = jsonencode({
    displayName = "Nigerian Audit AI Dashboard"
    mosaicLayout = {
      tiles = [
        {
          width  = 6
          height = 4
          widget = {
            title = "API Request Rate"
            scorecard = {
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "resource.type=\"cloud_run_revision\" AND resource.label.service_name=\"nigerian-audit-ai-api\""
                  aggregation = {
                    alignmentPeriod  = "60s"
                    perSeriesAligner = "ALIGN_RATE"
                  }
                }
              }
            }
          }
        }
      ]
    }
  })
}

---

# terraform/variables.tf
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "admin_email" {
  description = "Admin email for BigQuery access"
  type        = string
}

variable "api_key" {
  description = "API key for authentication"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}

variable "enable_monitoring" {
  description = "Enable monitoring and alerting"
  type        = bool
  default     = true
}

---

# terraform/outputs.tf
output "api_url" {
  description = "URL of the deployed API"
  value       = google_cloud_run_service.audit_ai_api.status[0].url
}

output "storage_bucket" {
  description = "Name of the storage bucket"
  value       = google_storage_bucket.audit_ai_bucket.name
}

output "bigquery_dataset" {
  description = "BigQuery dataset ID"
  value       = google_bigquery_dataset.audit_dataset.dataset_id
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.audit_ai_sa.email
}

output "project_id" {
  description = "GCP Project ID"
  value       = var.project_id
}

---

# tests/test_financial_analyzer.py
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.models.financial_analyzer import FinancialAnalyzer
from src.utils.currency import format_ngn, validate_ngn_amount

class TestFinancialAnalyzer:
    
    @pytest.fixture
    def analyzer(self):
        """Create FinancialAnalyzer instance for testing"""
        return FinancialAnalyzer()
    
    @pytest.fixture
    def sample_trial_balance(self):
        """Sample trial balance for testing"""
        return {
            "Cash and Bank": 5000000,
            "Accounts Receivable": 12000000,
            "Inventory": 8000000,
            "Property Plant Equipment": 25000000,
            "Accounts Payable": 4500000,
            "Long Term Loans": 15000000,
            "Share Capital": 20000000,
            "Sales Revenue": 30000000,
            "Cost of Sales": 18000000,
            "Operating Expenses": 8000000
        }
    
    def test_account_classification(self, analyzer, sample_trial_balance):
        """Test account classification functionality"""
        
        classification = analyzer.preprocess_trial_balance(sample_trial_balance)
        
        # Check that classification contains expected categories
        expected_categories = [
            'current_assets', 'non_current_assets', 'current_liabilities',
            'non_current_liabilities', 'equity', 'revenue', 'expenses'
        ]
        
        for category in expected_categories:
            assert category in classification
        
        # Check specific account classifications
        assert "Cash and Bank" in classification['current_assets']
        assert "Property Plant Equipment" in classification['non_current_assets']
        assert "Accounts Payable" in classification['current_liabilities']
        assert "Sales Revenue" in classification['revenue']
    
    def test_financial_ratio_calculation(self, analyzer, sample_trial_balance):
        """Test financial ratio calculations"""
        
        classification = analyzer.preprocess_trial_balance(sample_trial_balance)
        ratios = analyzer.calculate_financial_ratios(classification)
        
        # Check that key ratios are calculated
        expected_ratios = [
            'current_ratio', 'quick_ratio', 'debt_to_equity',
            'gross_profit_margin', 'net_profit_margin', 'return_on_assets'
        ]
        
        for ratio in expected_ratios:
            assert ratio in ratios
            assert isinstance(ratios[ratio], (int, float))
        
        # Check ratio values are reasonable
        assert ratios['current_ratio'] > 0
        assert 0 <= ratios['gross_profit_margin'] <= 1
    
    def test_financial_health_assessment(self, analyzer, sample_trial_balance):
        """Test financial health assessment"""
        
        classification = analyzer.preprocess_trial_balance(sample_trial_balance)
        ratios = analyzer.calculate_financial_ratios(classification)
        assessment = analyzer.assess_financial_health(ratios, "manufacturing")
        
        # Check assessment structure
        assert 'overall_score' in assessment
        assert 'risk_level' in assessment
        assert 'strengths' in assessment
        assert 'weaknesses' in assessment
        assert 'recommendations' in assessment
        
        # Check score is valid
        assert 0 <= assessment['overall_score'] <= 100
        assert assessment['risk_level'] in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    def test_currency_validation(self):
        """Test Nigerian currency validation"""
        
        # Valid amounts
        assert validate_ngn_amount(1000000) == True
        assert validate_ngn_amount("1000000") == True
        assert validate_ngn_amount("₦1,000,000") == True
        
        # Invalid amounts
        assert validate_ngn_amount(-1000) == False
        assert validate_ngn_amount("invalid") == False
        assert validate_ngn_amount(1e15) == False  # Too large
    
    def test_currency_formatting(self):
        """Test Nigerian currency formatting"""
        
        assert format_ngn(1000000) == "₦1,000,000.00"
        assert format_ngn(1234.56) == "₦1,234.56"
        assert format_ngn(0) == "₦0.00"
    
    def test_complete_analysis(self, analyzer, sample_trial_balance):
        """Test complete financial analysis workflow"""
        
        company_info = {
            "type": "manufacturing",
            "size": "medium",
            "name": "Test Manufacturing Company"
        }
        
        result = analyzer.analyze_financial_data(sample_trial_balance, company_info)
        
        # Check result structure
        assert 'classification' in result
        assert 'ratios' in result
        assert 'assessment' in result
        assert 'summary' in result
        
        # Check summary contains formatted amounts
        assert '₦' in result['summary']['total_assets']
        assert '₦' in result['summary']['total_liabilities']
    
    def test_nigerian_compliance_flags(self, analyzer):
        """Test Nigerian-specific compliance flag detection"""
        
        # High leverage scenario
        high_leverage_ratios = {
            'current_ratio': 0.5,  # Below 1.0
            'debt_to_equity': 2.5,  # High leverage
            'net_profit_margin': -0.05  # Negative margin
        }
        
        assessment = analyzer.assess_financial_health(high_leverage_ratios)
        
        # Should have compliance flags
        assert len(assessment['compliance_flags']) > 0
        assert any('ratio' in flag.lower() for flag in assessment['compliance_flags'])
    
    def test_industry_benchmarks(self, analyzer):
        """Test industry-specific benchmark application"""
        
        # Test manufacturing benchmarks
        manufacturing_benchmarks = analyzer.nigerian_ratios.get_benchmarks("manufacturing")
        assert 'current_ratio' in manufacturing_benchmarks
        assert 'inventory_turnover' in manufacturing_benchmarks
        
        # Test banking benchmarks
        banking_benchmarks = analyzer.nigerian_ratios.get_benchmarks("banking")
        assert 'capital_adequacy_ratio' in banking_benchmarks
        
        # Test that different industries have different benchmarks
        assert manufacturing_benchmarks != banking_benchmarks

---

# tests/test_compliance_checker.py
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.models.compliance_checker import ComplianceChecker
from src.schemas.compliance import ComplianceStatus, ViolationSeverity

class TestComplianceChecker:
    
    @pytest.fixture
    def compliance_checker(self):
        """Create ComplianceChecker instance for testing"""
        return ComplianceChecker()
    
    @pytest.fixture
    def sample_company_data(self):
        """Sample company data for testing"""
        return {
            "cac_number": "RC123456",
            "tin_number": "123456789012",
            "business_type": "limited_liability",
            "is_public": False,
            "industry": "manufacturing"
        }
    
    @pytest.fixture
    def sample_financial_data(self):
        """Sample financial data for testing"""
        return {
            "annual_revenue": 50000000,
            "total_assets": 80000000,
            "employee_count": 150,
            "financial_statements_filed": True,
            "ifrs_compliant": True,
            "vat_registered": True,
            "tax_returns_filed": True,
            "annual_returns_filed": True
        }
    
    def test_frc_compliance_check(self, compliance_checker, sample_company_data, sample_financial_data):
        """Test FRC compliance checking"""
        
        result = compliance_checker._check_frc_compliance(sample_company_data, sample_financial_data)
        
        # Check result structure
        assert 'regulation' in result
        assert 'status' in result
        assert 'score' in result
        assert 'violations' in result
        assert 'requirements_met' in result
        
        assert result['regulation'] == 'FRC'
        assert isinstance(result['score'], (int, float))
        assert 0 <= result['score'] <= 100
    
    def test_firs_compliance_check(self, compliance_checker, sample_company_data, sample_financial_data):
        """Test FIRS compliance checking"""
        
        result = compliance_checker._check_firs_compliance(sample_company_data, sample_financial_data)
        
        assert result['regulation'] == 'FIRS'
        assert isinstance(result['violations'], list)
        assert isinstance(result['requirements_met'], list)
    
    def test_cama_compliance_check(self, compliance_checker, sample_company_data, sample_financial_data):
        """Test CAMA compliance checking"""
        
        result = compliance_checker._check_cama_compliance(sample_company_data, sample_financial_data)
        
        assert result['regulation'] == 'CAMA'
        assert result['status'] in [status.value for status in ComplianceStatus]
    
    def test_invalid_cac_number(self, compliance_checker, sample_financial_data):
        """Test handling of invalid CAC number"""
        
        invalid_company_data = {
            "cac_number": "INVALID123",  # Invalid format
            "tin_number": "123456789012",
            "business_type": "limited_liability"
        }
        
        result = compliance_checker._check_cama_compliance(invalid_company_data, sample_financial_data)
        
        # Should have violations for invalid CAC
        assert len(result['violations']) > 0
        violation_types = [v['violation_type'] for v in result['violations']]
        assert any('CAC' in vtype for vtype in violation_types)
    
    def test_invalid_tin_number(self, compliance_checker, sample_financial_data):
        """Test handling of invalid TIN number"""
        
        invalid_company_data = {
            "cac_number": "RC123456",
            "tin_number": "12345",  # Too short
            "business_type": "limited_liability"
        }
        
        result = compliance_checker._check_firs_compliance(invalid_company_data, sample_financial_data)
        
        # Should have violations for invalid TIN
        assert len(result['violations']) > 0
        violation_types = [v['violation_type'] for v in result['violations']]
        assert any('TIN' in vtype for vtype in violation_types)
    
    def test_comprehensive_compliance_check(self, compliance_checker, sample_company_data, sample_financial_data):
        """Test comprehensive compliance check across multiple regulations"""
        
        regulations = ['FRC', 'FIRS', 'CAMA']
        
        result = compliance_checker.check_compliance(
            sample_company_data, 
            sample_financial_data, 
            regulations
        )
        
        # Check overall structure
        assert 'overview' in result
        assert 'detailed_results' in result
        assert 'recommendations' in result
        
        # Check overview
        overview = result['overview']
        assert 'overall_status' in overview
        assert 'overall_score' in overview
        assert 'total_violations' in overview
        assert overview['regulations_checked'] == regulations
        
        # Check detailed results
        assert len(result['detailed_results']) == len(regulations)
        for detail_result in result['detailed_results']:
            assert detail_result['regulation'] in regulations
    
    def test_high_risk_scenario(self, compliance_checker):
        """Test compliance check with high-risk company"""
        
        high_risk_company = {
            "cac_number": "INVALID",  # Invalid
            "tin_number": "123",      # Invalid
            "business_type": "limited_liability",
            "is_public": True,
            "annual_revenue": 2000000000  # Large company
        }
        
        poor_financial_data = {
            "annual_revenue": 2000000000,
            "total_assets": 1000000000,
            "financial_statements_filed": False,
            "ifrs_compliant": False,
            "vat_registered": False,
            "tax_returns_filed": False,
            "annual_returns_filed": False
        }
        
        result = compliance_checker.check_compliance(
            high_risk_company,
            poor_financial_data,
            ['FRC', 'FIRS', 'CAMA']
        )
        
        # Should have multiple violations and poor score
        assert result['overview']['total_violations'] > 0
        assert result['overview']['overall_score'] < 60
        assert result['overview']['overall_status'] != ComplianceStatus.COMPLIANT
    
    def test_banking_cbr_compliance(self, compliance_checker):
        """Test CBN compliance for banking institutions"""
        
        bank_company_data = {
            "cac_number": "RC789012",
            "tin_number": "789012345678",
            "business_type": "banking",
            "is_public": True
        }
        
        bank_financial_data = {
            "annual_revenue": 500000000,
            "total_assets": 5000000000,
            "capital_adequacy_ratio": 0.12,  # Below 15% requirement
            "liquidity_ratio": 0.25         # Below 30% requirement
        }
        
        result = compliance_checker._check_cbn_compliance(bank_company_data, bank_financial_data)
        
        # Should have CBN violations for low ratios
        assert len(result['violations']) > 0
        violation_types = [v['violation_type'] for v in result['violations']]
        assert any('Capital' in vtype or 'Liquidity' in vtype for vtype in violation_types)

---

# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.api.main import app
from src.config.settings import settings

class TestAPI:
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self):
        """Authentication headers for API requests"""
        return {"Authorization": f"Bearer {settings.API_KEY}"}
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "models_loaded" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Nigerian Audit AI API"
        assert data["status"] == "operational"
    
    def test_financial_analysis_endpoint(self, client, auth_headers):
        """Test financial analysis endpoint"""
        
        trial_balance = {
            "Cash and Bank": 5000000,
            "Accounts Receivable": 12000000,
            "Inventory": 8000000,
            "Property Plant Equipment": 25000000,
            "Accounts Payable": 4500000,
            "Sales Revenue": 30000000,
            "Cost of Sales": 18000000
        }
        
        request_data = {
            "trial_balance": trial_balance,
            "company_info": {
                "type": "manufacturing",
                "size": "medium"
            }
        }
        
        response = client.post(
            "/api/v1/analyze/financial",
            json=request_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "classification" in data["data"]
        assert "ratios" in data["data"]
    
    def test_compliance_check_endpoint(self, client, auth_headers):
        """Test compliance check endpoint"""
        
        request_data = {
            "company_data": {
                "cac_number": "RC123456",
                "tin_number": "123456789012",
                "business_type": "limited_liability",
                "is_public": False
            },
            "financial_data": {
                "annual_revenue": 50000000,
                "total_assets": 80000000,
                "employee_count": 150
            },
            "regulations": ["FRC", "FIRS", "CAMA"]
        }
        
        response = client.post(
            "/api/v1/compliance/check",
            json=request_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
    
    def test_validation_endpoints(self, client, auth_headers):
        """Test Nigerian data validation endpoints"""
        
        # Test CAC validation
        response = client.post(
            "/api/v1/validate/nigerian",
            json={"cac_number": "RC123456"},
            params={"validation_type": "cac"},
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Test TIN validation
        response = client.post(
            "/api/v1/validate/nigerian", 
            json={"tin_number": "123456789012"},
            params={"validation_type": "tin"},
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_unauthorized_access(self, client):
        """Test unauthorized access to protected endpoints"""
        
        response = client.post("/api/v1/analyze/financial", json={})
        assert response.status_code == 401
    
    def test_invalid_api_key(self, client):
        """Test invalid API key"""
        
        invalid_headers = {"Authorization": "Bearer invalid-key"}
        response = client.post(
            "/api/v1/analyze/financial",
            json={},
            headers=invalid_headers
        )
        assert response.status_code == 401
    
    def test_malformed_request(self, client, auth_headers):
        """Test malformed request handling"""
        
        # Missing required fields
        response = client.post(
            "/api/v1/analyze/financial",
            json={"invalid": "data"},
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error