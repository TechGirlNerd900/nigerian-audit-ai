from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App Configuration
    APP_NAME: str = "Nigerian Audit AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    REDIS_URL: str
    
    # GCP Configuration
    GOOGLE_CLOUD_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    GCP_REGION: str = "us-central1"
    GCS_BUCKET: str
    
    # Nigerian APIs
    FIRS_API_KEY: str
    FIRS_API_URL: str = "https://atrs-api.firs.gov.ng"
    CAC_API_KEY: Optional[str] = None
    NGX_API_KEY: Optional[str] = None
    
    # Security
    JWT_SECRET: str
    API_KEY: str
    
    # ML Configuration
    MODEL_VERSION: str = "v1.0"
    TRAINING_BATCH_SIZE: int = 32
    LEARNING_RATE: float = 0.001
    
    # Nigerian Specific
    DEFAULT_CURRENCY: str = "NGN"
    VAT_RATE: float = 0.075  # 7.5%
    CIT_RATE_SMALL: float = 0.0   # 0% for small companies
    CIT_RATE_MEDIUM: float = 0.20  # 20% for medium companies
    CIT_RATE_LARGE: float = 0.30   # 30% for large companies
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()