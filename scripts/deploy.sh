# scripts/deploy.sh
#!/bin/bash

# Nigerian Audit AI Deployment Script

set -e

echo "🇳🇬 Deploying Nigerian Audit AI to Google Cloud Platform..."

# Check prerequisites
echo "Checking prerequisites..."
command -v gcloud >/dev/null 2>&1 || { echo "gcloud CLI required but not installed"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker required but not installed"; exit 1; }

# Set variables
PROJECT_ID=${GOOGLE_CLOUD_PROJECT_ID:-$(gcloud config get-value project)}
REGION=${GCP_REGION:-us-central1}
SERVICE_NAME="nigerian-audit-ai-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/nigerian-audit-ai"

echo "Project ID: ${PROJECT_ID}"
echo "Region: ${REGION}"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t ${IMAGE_NAME}:latest .

# Push to Google Container Registry
echo "📤 Pushing image to GCR..."
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image=${IMAGE_NAME}:latest \
    --platform=managed \
    --region=${REGION} \
    --allow-unauthenticated \
    --memory=4Gi \
    --cpu=2 \
    --timeout=300 \
    --concurrency=100 \
    --min-instances=1 \
    --max-instances=10 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT_ID=${PROJECT_ID},GCP_REGION=${REGION}"

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')

echo "✅ Deployment completed successfully!"
echo "🌐 API URL: ${SERVICE_URL}"
echo "📖 API Documentation: ${SERVICE_URL}/docs"
echo "❤️ Health Check: ${SERVICE_URL}/health"

# Test deployment
echo "🧪 Testing deployment..."
curl -f "${SERVICE_URL}/health" || echo "⚠️ Health check failed"

echo "🎉 Nigerian Audit AI deployment completed!"

---

# docs/api.md
# Nigerian Audit AI - API Documentation

## Overview

The Nigerian Audit AI provides a comprehensive RESTful API for financial analysis, compliance checking, and risk assessment specifically designed for Nigerian businesses and regulations.

## Base URL

```
Production: https://nigerian-audit-ai-xxxxx-uc.a.run.app
Development: http://localhost:8000
```

## Authentication

All API endpoints require Bearer token authentication:

```bash
curl -H "Authorization: Bearer your-api-key" \
     https://api-url/endpoint
```

## Core Endpoints

### Financial Analysis

#### Analyze Financial Data
```http
POST /api/v1/analyze/financial
```

Performs comprehensive financial analysis of trial balance data.

**Request Body:**
```json
{
  "trial_balance": {
    "Cash and Bank": 5000000,
    "Accounts Receivable": 12000000,
    "Inventory": 8000000,
    "Property Plant Equipment": 25000000,
    "Accounts Payable": 4500000,
    "Sales Revenue": 30000000,
    "Cost of Sales": 18000000
  },
  "company_info": {
    "type": "manufacturing",
    "size": "medium",
    "industry": "consumer_goods"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "classification": {
      "current_assets": {"Cash and Bank": "₦5,000,000.00"},
      "revenue": {"Sales Revenue": "₦30,000,000.00"}
    },
    "ratios": {
      "current_ratio": 2.5,
      "debt_to_equity": 0.4,
      "net_profit_margin": 0.15
    },
    "assessment": {
      "overall_score": 85,
      "risk_level": "LOW",
      "strengths": ["Strong liquidity position"],
      "recommendations": ["Continue current financial management"]
    }
  }
}
```

### Compliance Checking

#### Check Compliance
```http
POST /api/v1/compliance/check
```

Checks compliance against Nigerian regulations (FRC, FIRS, CAMA, CBN).

**Request Body:**
```json
{
  "company_data": {
    "cac_number": "RC123456",
    "tin_number": "123456789012", 
    "business_type": "limited_liability",
    "is_public": false
  },
  "financial_data": {
    "annual_revenue": 50000000,
    "total_assets": 80000000,
    "employee_count": 150
  },
  "regulations": ["FRC", "FIRS", "CAMA"]
}
```

### Data Validation

#### Validate CAC Number
```http
POST /api/v1/validate/cac
```

#### Validate TIN Number  
```http
POST /api/v1/validate/tin
```

#### Validate Phone Number
```http
POST /api/v1/validate/phone
```

## Error Handling

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error description",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limits

- 100 requests per minute per API key
- Burst limit: 200 requests per minute
- Daily limit: 10,000 requests

## Nigerian-Specific Features

### Currency Handling
- All amounts in Nigerian Naira (₦)
- Automatic formatting: `₦1,000,000.00`
- Validation for reasonable amounts

### Regulatory Compliance
- **FRC**: Financial Reporting Council requirements
- **FIRS**: Tax compliance and TIN validation
- **CAMA**: Company registration compliance
- **CBN**: Banking sector requirements

### Industry Benchmarks
- Manufacturing sector ratios
- Banking sector prudential guidelines
- Oil & gas sector metrics
- Telecommunications benchmarks

## SDK Examples

### Python
```python
import requests

api_key = "your-api-key"
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.post(
    "https://api-url/api/v1/analyze/financial",
    json=trial_balance_data,
    headers=headers
)

result = response.json()
```

### JavaScript
```javascript
const response = await fetch('/api/v1/analyze/financial', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(trialBalanceData)
});

const result = await response.json();
```

---

# docs/deployment.md
# Deployment Guide

## Prerequisites

- Google Cloud Platform account
- Docker installed
- Google Cloud SDK installed
- Terraform (optional, for infrastructure)

## Quick Deployment

### 1. Setup GCP
```bash
gcloud auth login
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID
```

### 2. Deploy with Script
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## Manual Deployment

### 1. Build and Push Image
```bash
docker build -t gcr.io/$PROJECT_ID/nigerian-audit-ai .
docker push gcr.io/$PROJECT_ID/nigerian-audit-ai
```

### 2. Deploy to Cloud Run
```bash
gcloud run deploy nigerian-audit-ai \
  --image gcr.io/$PROJECT_ID/nigerian-audit-ai \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2
```

## Infrastructure as Code

### Using Terraform
```bash
cd terraform
terraform init
terraform plan -var="project_id=$PROJECT_ID"
terraform apply
```

## Environment Variables

Required environment variables:

```bash
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GCP_REGION=us-central1
API_KEY=your-secure-api-key
DATABASE_URL=postgresql://...
```

## Monitoring & Logging

The deployment includes:
- Cloud Monitoring dashboards
- Error reporting
- Performance metrics
- Audit logging

## Scaling Configuration

- **Min instances**: 1
- **Max instances**: 10  
- **CPU**: 2 cores
- **Memory**: 4GB
- **Timeout**: 300 seconds