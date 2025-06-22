#!/bin/bash

# Nigerian Audit AI Setup Script

echo "🇳🇬 Setting up Nigerian Audit AI System..."

# Check prerequisites
echo "Checking prerequisites..."
python --version || { echo "Python 3.8+ required"; exit 1; }
gcloud --version || { echo "Google Cloud SDK required"; exit 1; }

# Setup GCP
echo "Setting up Google Cloud Platform..."

# Enable APIs
echo "Enabling GCP APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable documentai.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Create storage bucket
echo "Creating GCS bucket..."
gsutil mb gs://${GOOGLE_CLOUD_PROJECT_ID}-nigerian-audit-ai

# Create BigQuery dataset
echo "Creating BigQuery dataset..."
bq mk --location=us-central1 nigerian_audit_ai

# Setup database
echo "Setting up PostgreSQL database..."
python scripts/setup_database.py

# Create directories
echo "Creating directories..."
mkdir -p data/{raw,processed,training,regulations}
mkdir -p models/{saved_models,checkpoints,exports}
mkdir -p logs

echo "✅ Setup completed successfully!"
echo "Next steps:"
echo "1. Configure your .env file"
echo "2. Run: python scripts/collect_data.py"
echo "3. Run: python scripts/train_models.py"
echo "4. Start API: uvicorn src.api.main:app --reload"