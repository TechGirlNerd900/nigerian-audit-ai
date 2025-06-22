import os
import logging
from google.cloud import storage, aiplatform, bigquery
from google.oauth2 import service_account
from .settings import settings

logger = logging.getLogger(__name__)

# GCP Clients
storage_client = None
aiplatform_client = None
bigquery_client = None

def initialize_gcp_clients():
    """Initialize Google Cloud Platform clients"""
    global storage_client, aiplatform_client, bigquery_client
    
    try:
        # Initialize credentials
        if settings.GOOGLE_APPLICATION_CREDENTIALS and os.path.exists(settings.GOOGLE_APPLICATION_CREDENTIALS):
            credentials = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_APPLICATION_CREDENTIALS
            )
        else:
            # Use default credentials (for Cloud Run, Compute Engine, etc.)
            credentials = None
        
        # Initialize Storage client
        storage_client = storage.Client(
            project=settings.GOOGLE_CLOUD_PROJECT_ID,
            credentials=credentials
        )
        
        # Initialize AI Platform
        aiplatform.init(
            project=settings.GOOGLE_CLOUD_PROJECT_ID,
            location=settings.GCP_REGION,
            credentials=credentials
        )
        
        # Initialize BigQuery client
        bigquery_client = bigquery.Client(
            project=settings.GOOGLE_CLOUD_PROJECT_ID,
            credentials=credentials
        )
        
        logger.info("GCP clients initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize GCP clients: {e}")
        return False

def get_storage_client():
    """Get Google Cloud Storage client"""
    if storage_client is None:
        initialize_gcp_clients()
    return storage_client

def get_bigquery_client():
    """Get BigQuery client"""
    if bigquery_client is None:
        initialize_gcp_clients()
    return bigquery_client

def upload_to_gcs(bucket_name: str, source_file_path: str, destination_blob_name: str):
    """Upload file to Google Cloud Storage"""
    try:
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        
        blob.upload_from_filename(source_file_path)
        logger.info(f"File {source_file_path} uploaded to {destination_blob_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to upload to GCS: {e}")
        return False

def download_from_gcs(bucket_name: str, source_blob_name: str, destination_file_path: str):
    """Download file from Google Cloud Storage"""
    try:
        client = get_storage_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        
        blob.download_to_filename(destination_file_path)
        logger.info(f"File {source_blob_name} downloaded to {destination_file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to download from GCS: {e}")
        return False

async def initializeGCP():
    """Async wrapper for GCP initialization"""
    return initialize_gcp_clients()