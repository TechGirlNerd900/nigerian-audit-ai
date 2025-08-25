# 🚀 GCP Training & Deployment Guide

## Step-by-Step Model Training on Google Cloud Platform

### 1. Initial GCP Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/nigerian-audit-ai.git
cd nigerian-audit-ai

# Set up environment
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values
```

### 2. GCP Project Setup

```bash
# Install Google Cloud SDK (if not already installed)
# Install Google Cloud SDK (if not already installed)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login and set project
gcloud auth login
export PROJECT_ID="model-463723" # Make sure this is correctly set to your actual project ID
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
    aiplatform.googleapis.com \
    storage.googleapis.com \
    bigquery.googleapis.com \
    documentai.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    compute.googleapis.com   

# Create service account
gcloud iam service-accounts create nigerian-audit-ai \
    --display-name="Nigerian Audit AI Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:nigerian-audit-ai@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:nigerian-audit-ai@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:nigerian-audit-ai@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

# Create and download service account key
gcloud iam service-accounts keys create ./gcp-service-account.json \
    --iam-account=nigerian-audit-ai@${PROJECT_ID}.iam.gserviceaccount.com

# Create storage bucket
gsutil mb gs://${PROJECT_ID}-nigerian-audit-ai

# Create BigQuery dataset
bq mk --location=us-central1 nigerian_audit_ai
```

### 3. Data Collection & Preparation

```bash
# Run the complete data collection pipeline
python scripts/collect_data.py

# This will:
# - Scrape NGX financial statements
# - Download FRC regulations
# - Collect training examples
# - Prepare datasets for ML training
```

### 4. Training Models on Vertex AI

Create `src/training/vertex_ai_trainer.py`:

```python
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic as aip
import os
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class VertexAITrainer:
    def __init__(self, project_id: str, region: str = "us-central1"):
        self.project_id = project_id
        self.region = region
        aiplatform.init(project=project_id, location=region)
    
    def create_training_job(self, model_type: str, config: Dict):
        """Create custom training job on Vertex AI"""
        
        display_name = f"nigerian-audit-{model_type}-training"
        
        # Define container spec
        container_spec = {
            "image_uri": f"gcr.io/{self.project_id}/nigerian-audit-trainer:latest",
            "command": [],
            "args": [
                "--model-type", model_type,
                "--epochs", str(config.get("epochs", 100)),
                "--batch-size", str(config.get("batch_size", 32)),
                "--learning-rate", str(config.get("learning_rate", 0.001))
            ]
        }
        
        # Define machine spec
        machine_spec = {
            "machine_type": "n1-standard-8",
            "accelerator_type": aip.AcceleratorType.NVIDIA_TESLA_T4,
            "accelerator_count": 1,
        }
        
        # Create training job
        job = aiplatform.CustomTrainingJob(
            display_name=display_name,
            container_spec=container_spec,
            requirements=["tensorflow==2.15.0", "scikit-learn==1.3.2"],
            model_serving_container_image_uri="gcr.io/cloud-aiplatform/prediction/tf2-cpu.2-8:latest",
        )
        
        # Submit job
        model = job.run(
            dataset=None,  # Using our custom data pipeline
            replica_count=1,
            machine_type="n1-standard-8",
            accelerator_type="NVIDIA_TESLA_T4",
            accelerator_count=1,
            base_output_dir=f"gs://{self.project_id}-nigerian-audit-ai/training-outputs",
            sync=True
        )
        
        logger.info(f"Training job completed. Model: {model.display_name}")
        return model
    
    def train_all_models(self):
        """Train all models sequentially"""
        
        models_config = {
            "financial_analysis": {
                "epochs": 100,
                "batch_size": 32,
                "learning_rate": 0.001
            },
            "compliance_checker": {
                "epochs": 50,
                "batch_size": 64,
                "learning_rate": 0.001
            },
            "risk_assessment": {
                "epochs": 75,
                "batch_size": 32,
                "learning_rate": 0.0005
            }
        }
        
        trained_models = {}
        
        for model_type, config in models_config.items():
            logger.info(f"Training {model_type} model...")
            model = self.create_training_job(model_type, config)
            trained_models[model_type] = model
        
        return trained_models

def main():
    trainer = VertexAITrainer(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        region=os.getenv("GCP_REGION", "us-central1")
    )
    
    trainer.train_all_models()

if __name__ == "__main__":
    main()
```

### 5. Build Training Container

Create `Dockerfile.training`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY data/ ./data/
COPY scripts/ ./scripts/

# Set Python path
ENV PYTHONPATH=/app

# Entry point for training
ENTRYPOINT ["python", "scripts/train_models.py"]
```

Build and push the training container:

```bash
# Build training container
docker build -f Dockerfile.training -t gcr.io/$PROJECT_ID/nigerian-audit-trainer:latest .

# Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/nigerian-audit-trainer:latest
```

### 6. Submit Training Jobs

```bash
# Train individual models locally
python scripts/train_models.py --model financial_analysis --epochs 50

# Train all models on Vertex AI
python scripts/train_models.py --vertex

# Train a specific model on Vertex AI
python scripts/train_models.py --model financial_analysis --vertex --epochs 100
```

### 7. Model Deployment

Create deployment script `scripts/deploy_models.py`:

```python
from google.cloud import aiplatform
import os
import logging

logger = logging.getLogger(__name__)

def deploy_model_to_endpoint(model_name: str, model_id: str):
    """Deploy trained model to Vertex AI endpoint"""
    
    # Initialize Vertex AI
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GCP_REGION", "us-central1")
    )
    
    # Get the model
    model = aiplatform.Model(model_name=model_id)
    
    # Create endpoint
    endpoint = aiplatform.Endpoint.create(
        display_name=f"nigerian-audit-{model_name}-endpoint",
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GCP_REGION", "us-central1")
    )
    
    # Deploy model to endpoint
    model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=f"{model_name}-v1",
        machine_type="n1-standard-4",
        min_replica_count=1,
        max_replica_count=3,
        accelerator_type=None,  # Use CPU for inference
        accelerator_count=0,
    )
    
    logger.info(f"Model {model_name} deployed to endpoint: {endpoint.resource_name}")
    return endpoint

def main():
    # Deploy all trained models
    models_to_deploy = [
        ("financial_analysis", "projects/PROJECT_ID/locations/us-central1/models/MODEL_ID"),
        ("compliance_checker", "projects/PROJECT_ID/locations/us-central1/models/MODEL_ID"),
        ("risk_assessment", "projects/PROJECT_ID/locations/us-central1/models/MODEL_ID"),
    ]
    
    for model_name, model_id in models_to_deploy:
        deploy_model_to_endpoint(model_name, model_id)

if __name__ == "__main__":
    main()
```

### 8. API Deployment on Cloud Run

```bash
# Build API container
docker build -t gcr.io/$PROJECT_ID/nigerian-audit-api:latest .

# Push to registry
docker push gcr.io/$PROJECT_ID/nigerian-audit-api:latest

# Deploy to Cloud Run
gcloud run deploy nigerian-audit-api \
    --image gcr.io/$PROJECT_ID/nigerian-audit-api:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 300 \
    --concurrency 100 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID" \
    --set-env-vars="GCP_REGION=us-central1"
```

### 9. Automated CI/CD Pipeline

Create `cloudbuild.yaml`:

```yaml
steps:
  # Build training container
  - name: 'gcr.io/cloud-builders/docker'
    args: [
      'build', 
      '-f', 'Dockerfile.training',
      '-t', 'gcr.io/$PROJECT_ID/nigerian-audit-trainer:$BUILD_ID',
      '-t', 'gcr.io/$PROJECT_ID/nigerian-audit-trainer:latest',
      '.'
    ]

  # Push training container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/nigerian-audit-trainer:latest']

  # Build API container
  - name: 'gcr.io/cloud-builders/docker'
    args: [
      'build',
      '-t', 'gcr.io/$PROJECT_ID/nigerian-audit-api:$BUILD_ID',
      '-t', 'gcr.io/$PROJECT_ID/nigerian-audit-api:latest',
      '.'
    ]

  # Push API container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/nigerian-audit-api:latest']

  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'nigerian-audit-api',
      '--image', 'gcr.io/$PROJECT_ID/nigerian-audit-api:latest',
      '--region', 'us-central1',
      '--platform', 'managed',
      '--allow-unauthenticated',
      '--memory', '4Gi',
      '--cpu', '2'
    ]

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'E2_HIGHCPU_8'

timeout: 1800s
```

Set up automated builds:

```bash
# Connect repository to Cloud Build
gcloud builds triggers create github \
    --repo-name="nigerian-audit-ai" \
    --repo-owner="yourusername" \
    --branch-pattern="^main$" \
    --build-config="cloudbuild.yaml"
```

### 10. Monitoring & Logging

Set up monitoring dashboard:

```python
# scripts/setup_monitoring.py
from google.cloud import monitoring_v3
import time

def create_custom_metrics():
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}"
    
    # Define custom metrics
    metrics = [
        {
            "type": "custom.googleapis.com/nigerian_audit/prediction_accuracy",
            "labels": [
                {"key": "model_type", "value_type": "STRING"},
                {"key": "prediction_class", "value_type": "STRING"}
            ],
            "metric_kind": "GAUGE",
            "value_type": "DOUBLE",
            "description": "Prediction accuracy for Nigerian audit models"
        },
        {
            "type": "custom.googleapis.com/nigerian_audit/compliance_violations",
            "labels": [
                {"key": "regulation_type", "value_type": "STRING"},
                {"key": "severity", "value_type": "STRING"}
            ],
            "metric_kind": "CUMULATIVE",
            "value_type": "INT64",
            "description": "Count of compliance violations detected"
        }
    ]
    
    for metric_descriptor in metrics:
        descriptor = monitoring_v3.MetricDescriptor(
            type=metric_descriptor["type"],
            metric_kind=metric_descriptor["metric_kind"],
            value_type=metric_descriptor["value_type"],
            description=metric_descriptor["description"]
        )
        
        # Add labels
        for label in metric_descriptor["labels"]:
            descriptor.labels.append(
                monitoring_v3.LabelDescriptor(
                    key=label["key"],
                    value_type=label["value_type"]
                )
            )
        
        # Create the metric descriptor
        client.create_metric_descriptor(
            name=project_name,
            metric_descriptor=descriptor
        )

if __name__ == "__main__":
    create_custom_metrics()
```

### 11. Testing the System

Create comprehensive tests:

```python
# tests/test_integration.py
import pytest
import requests
import os
from src.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_financial_analysis():
    """Test financial analysis endpoint"""
    
    trial_balance = {
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
    
    response = client.post(
        "/api/v1/analyze/financial",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
        json={
            "trial_balance": trial_balance,
            "company_info": {
                "type": "manufacturing",
                "size": "medium"
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "classification" in data["data"]
    assert "ratios" in data["data"]
    assert "assessment" in data["data"]

def test_compliance_check():
    """Test compliance checking endpoint"""
    
    response = client.post(
        "/api/v1/compliance/check",
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
        json={
            "company_data": {
                "cac_number": "RC123456",
                "tin_number": "123456789012",
                "business_type": "limited_liability"
            },
            "financial_data": {
                "annual_revenue": 50000000,
                "total_assets": 80000000
            },
            "regulations": ["FRC", "FIRS", "CAMA"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

# Run tests
if __name__ == "__main__":
    pytest.main([__file__])
```

### 12. Production Deployment Checklist

- [ ] Environment variables configured
- [ ] GCP services enabled and configured
- [ ] Training data collected and processed
- [ ] Models trained and validated
- [ ] API endpoints tested
- [ ] Authentication implemented
- [ ] Rate limiting configured
- [ ] Monitoring and alerting set up
- [ ] Error logging implemented
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] Documentation updated

### 13. Usage Examples

Once deployed, you can use the API:

```python
import requests

# API endpoint from Cloud Run
API_URL = "https://nigerian-audit-api-xxxxx-uc.a.run.app"
API_KEY = "your-api-key"

# Analyze financial data
response = requests.post(
    f"{API_URL}/api/v1/analyze/financial",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "trial_balance": {
            "Cash": 5000000,
            "Accounts Receivable": 12000000,
            "Revenue": 30000000,
            # ... more accounts
        },
        "company_info": {"type": "manufacturing"}
    }
)

result = response.json()
print(f"Financial Health Score: {result['data']['assessment']['overall_score']}")
```

### 14. Cost Optimization

- Use preemptible instances for training
- Set up auto-scaling for Cloud Run
- Implement model caching
- Use regional storage for data
- Monitor and optimize resource usage

### 15. Maintenance

- Regular model retraining
- Regulatory updates monitoring
- Performance monitoring
- Security updates
- Data pipeline maintenance

This complete setup provides a production-ready Nigerian Audit AI system on GCP with proper training, deployment, and monitoring capabilities.


COMMAND LINE

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
##
cp .env.example .env
# Now edit the .env file with your values

# Google Cloud Platform (GCP) Setup:

# Log in to your Google Cloud account and set your project ID:
  Bash

gcloud auth login
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

chmod +x scripts/setup.sh
./scripts/setup.sh

## db Initialize the project's database by running:

python scripts/setup_database.py


# Run the data collection script to populate the data directory:
Bash

python scripts/collect_data.py

## Running the Application:

## You can now run the FastAPI application locally for development:
Bash

uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000