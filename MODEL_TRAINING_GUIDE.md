# Nigerian Audit AI - Model Training Guide

This guide provides step-by-step instructions for training the AI models using the actual training script.

## Prerequisites

Before training models, ensure you have:

1. **Python 3.10+** installed
2. **Poetry** for dependency management
3. **Google Cloud Platform** account with:
   - Project created
   - Service account with appropriate permissions
   - Cloud Storage bucket created
   - Vertex AI API enabled (if using cloud training)
4. **Environment variables** configured in `.env` file

## Step 1: Environment Setup

### 1.1 Install Dependencies
```bash
poetry install
```

### 1.2 Configure Environment Variables

**Minimal setup for training (create `.env` file with these):**

```env
# ML Configuration (Required for training)
MODEL_VERSION=v1.0
TRAINING_BATCH_SIZE=32
LEARNING_RATE=0.001

# Nigerian Tax Rates (Required for compliance model)
VAT_RATE=0.075
CIT_RATE_SMALL=0.0
CIT_RATE_MEDIUM=0.20
CIT_RATE_LARGE=0.30
```

**Optional variables (only add if you need these features):**

```env
# Database (only needed if storing real data)
# DATABASE_URL=postgresql://user:password@host:port/dbname
# REDIS_URL=redis://localhost:6379

# GCP Configuration (only needed for cloud training/storage)
# GOOGLE_CLOUD_PROJECT_ID=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
# GCP_REGION=us-central1
# GCS_BUCKET=your-bucket-name

# Nigerian APIs (only needed for live data scraping - NOT required for training)
# FIRS_API_KEY=your-firs-api-key
# FIRS_API_URL=https://atrs-api.firs.gov.ng

# Security (only needed for API deployment)
# JWT_SECRET=your-jwt-secret-key
# API_KEY=your-api-key
```

## Step 2: Web Scraping for Real Training Data

The system includes powerful scrapers for Nigerian financial sources. Here's how to collect real data:

### 2.1 Available Data Sources

**Nigerian Regulatory Bodies:**
- **NGX (Nigerian Exchange)**: Listed companies, financial statements, market data
- **FRC (Financial Reporting Council)**: Regulations, standards, compliance documents
- **CAC (Corporate Affairs Commission)**: Company registration data
- **FIRS (Federal Inland Revenue Service)**: Tax regulations, finance acts
- **CBN (Central Bank of Nigeria)**: Banking regulations, monetary policy

**International Standards:**
- **IFRS Foundation**: International Financial Reporting Standards
- **IAASB**: International Standards on Auditing
- **Deloitte/KPMG**: Illustrative financial statements

### 2.2 Scraping Setup

Install additional dependencies for web scraping:

```bash
# Install Playwright for dynamic content
poetry run playwright install

# Install additional scraping tools
poetry add playwright beautifulsoup4 lxml requests-html
```

### 2.3 Collect Real Data

**Full data collection (recommended for production training):**

```bash
poetry run python scripts/train_models.py --collect-data
```

This will scrape:
- NGX listed companies and their financials
- FRC regulatory documents (PDFs and HTML)
- CAC company registration data
- Direct downloads of Nigerian legislation
- International accounting standards

**Manual data collection:**

```bash
# Run data collection separately
poetry run python scripts/collect_data.py

# Then train with collected data
poetry run python scripts/train_models.py
```

### 2.4 Specific Scraper Usage

**NGX Scraper (Stock Exchange Data):**
```python
from src.scrapers.ngx_scraper import NGXScraper

ngx = NGXScraper()
# Get all listed companies
companies = ngx.scrape(mode="listed_companies")
# Get specific company financials
financials = ngx.scrape(mode="company_financials", symbol="ZENITHBANK")
```

**FRC Scraper (Regulatory Documents):**
```python
from src.scrapers.frc_scraper import FRCScraper

async with FRCScraper() as frc:
    documents = await frc.collect_data()
    # Downloads PDFs and HTML content from FRC website
```

**CAC Scraper (Company Registration):**
```python
from src.scrapers.cac_scraper import CACScraper

cac = CACScraper()
company_data = cac.scrape("RC123456")  # Registration number
```

### 2.5 Data Storage Structure

Scraped data is organized as:

```
data/
├── raw/                    # Raw scraped data
│   ├── ngx_companies.json
│   ├── frc_documents/
│   ├── cac_registrations.json
│   └── regulatory_pdfs/
├── processed/              # Cleaned data
│   ├── financial_statements.csv
│   ├── compliance_rules.json
│   └── company_profiles.csv
├── training/               # ML-ready datasets
│   ├── financial_training_data.json
│   ├── compliance_training_data.json
│   └── trial_balance_training_data.json
└── regulations/            # Regulatory documents
    ├── processed_regulations.json
    └── ifrs_standards/
```

### 2.6 Quick Start (Synthetic Data)

If you want to start immediately without scraping:

```bash
poetry run python scripts/train_models.py
```

This generates synthetic data and trains models locally.

## Step 3: Model Training Options

The training script supports several options:

### 3.1 Train All Models (Default)
```bash
poetry run python scripts/train_models.py
```

### 3.2 Train Specific Models
```bash
# Train only financial analysis model
poetry run python scripts/train_models.py --model financial

# Train only compliance checker
poetry run python scripts/train_models.py --model compliance

# Train only risk assessment model
poetry run python scripts/train_models.py --model risk

# Train only document processor
poetry run python scripts/train_models.py --model document
```

### 3.3 Custom Training Parameters
```bash
# Custom epochs and batch size
poetry run python scripts/train_models.py --epochs 150 --batch-size 64

# Train on Vertex AI (cloud)
poetry run python scripts/train_models.py --vertex

# Collect fresh data and train
poetry run python scripts/train_models.py --collect-data --epochs 100
```

## Step 4: Available Models

The system trains these models:

### 4.1 Financial Analysis Model
- **Purpose**: Analyzes financial statements and calculates risk levels
- **Input**: Financial ratios (current ratio, debt-to-equity, profit margins, etc.)
- **Output**: Risk classification (Low, Medium, High, Critical)
- **Architecture**: Neural network with dropout layers

### 4.2 Compliance Checker Model
- **Purpose**: Identifies potential regulatory violations
- **Input**: Company data (size, industry, revenue, assets, etc.)
- **Output**: Multi-label classification for violations (FRC, FIRS, CAMA, CBN)
- **Architecture**: Multi-label neural network

### 4.3 Trial Balance Classification Model
- **Purpose**: Classifies trial balance accounts automatically
- **Input**: Account codes and names
- **Output**: Account classifications
- **Architecture**: Text embedding with neural network

### 4.4 Document Intelligence Model
- **Purpose**: Processes and classifies financial documents
- **Input**: Document text content
- **Output**: Document type classification
- **Architecture**: Text tokenization with neural network

## Step 4.5: Real Data Sources

When using `--collect-data`, the system scrapes:

**From NGX (Nigerian Exchange):**
- Listed company symbols and names
- Financial statements (revenue, profit, assets)
- Annual reports (PDF links)
- Market capitalization data

**From FRC (Financial Reporting Council):**
- Nigerian Code of Corporate Governance
- Financial reporting standards
- Compliance guidelines
- Regulatory updates

**From Direct Sources:**
- CAMA 2020 (Companies and Allied Matters Act)
- Finance Acts 2019-2023
- FIRS Transfer Pricing Regulations
- CBN Banking Guidelines
- IFRS Standards (IAS 1, 2, 7, 8, 10, 12, 16, etc.)
- Illustrative financial statements

**Training Data Generated:**
- 1000+ financial analysis examples (from real company patterns)
- 500+ compliance examples (based on actual regulations)
- 800+ risk assessment cases
- Trial balance accounts (Nigerian chart of accounts)
- Document classification samples

## Step 5: Training Process Details

### 5.1 Data Generation
The system generates synthetic training data including:
- 1000 financial analysis examples
- 500 compliance examples
- 800 risk assessment examples
- Trial balance accounts with Nigerian accounting standards
- Document intelligence samples

### 5.2 Model Architecture
Each model uses:
- **TensorFlow/Keras** framework
- **StandardScaler** for feature normalization
- **Early stopping** to prevent overfitting
- **Learning rate reduction** on plateau
- **Model checkpointing** for best weights

### 5.3 Training Features
- Automatic train/test splitting (80/20)
- Cross-validation
- Performance metrics logging
- Model versioning
- Cloud storage integration

## Step 6: Model Storage

### 6.1 Local Storage
Trained models are saved to:
- `models/saved_models/` - Final trained models
- `models/checkpoints/` - Training checkpoints
- `models/exports/` - Export-ready models

### 6.2 Cloud Storage (GCS)
Models are automatically uploaded to Google Cloud Storage:
- Bucket: Specified in `GCS_BUCKET` environment variable
- Path: `models/{model_name}/{version}/`
- Includes: Model files, scalers, encoders

## Step 7: Monitoring Training

### 7.1 Training Logs
Monitor training progress through console output:
```
🇳🇬 Starting Nigerian Audit AI Model Training
Model: all
Epochs: 100
Batch Size: 32
Train on Vertex AI: False

📊 Collecting training data...
Training financial analysis model...
Training compliance checker model...
Training trial balance classification model...
Training document intelligence model...

✅ Model training completed!
```

### 7.2 Model Performance
Each model outputs:
- Training/validation accuracy
- Loss curves
- Classification reports
- Confusion matrices

## Step 8: Vertex AI Training (Cloud)

### 8.1 Enable Vertex AI Training
```bash
poetry run python scripts/train_models.py --vertex
```

### 8.2 Requirements for Vertex AI
- Vertex AI API enabled in GCP
- Appropriate IAM permissions
- Container registry access
- Sufficient compute quotas

## Step 9: Troubleshooting

### 9.1 Common Issues

**Memory Errors:**
```bash
# Reduce batch size
poetry run python scripts/train_models.py --batch-size 16
```

**GCP Authentication:**
```bash
# Verify credentials
gcloud auth application-default login
```

**Missing Dependencies:**
```bash
# Reinstall dependencies
poetry install --no-cache
```

### 9.2 Missing API Keys
If you don't have FIRS or other API keys:
```bash
# Train with synthetic data only (recommended)
poetry run python scripts/train_models.py

# Skip data collection entirely
poetry run python scripts/train_models.py --model all
```

### 9.3 Data Issues
If training data is insufficient:
- Increase synthetic data generation in `data_collector.py`
- Add real data sources
- Adjust data collection parameters

## Step 10: Next Steps

After training:
1. **Test Models**: Use the trained models in the API
2. **Monitor Performance**: Track model accuracy in production
3. **Retrain**: Periodically retrain with new data
4. **Deploy**: Use the models in the FastAPI application

## Command Reference

```bash
# Basic training
poetry run python scripts/train_models.py

# All options
poetry run python scripts/train_models.py \
  --model all \
  --epochs 100 \
  --batch-size 32 \
  --collect-data \
  --vertex

# Individual model training
poetry run python scripts/train_models.py --model financial
poetry run python scripts/train_models.py --model compliance
poetry run python scripts/train_models.py --model risk
poetry run python scripts/train_models.py --model document
```

## File Structure After Training

```
nigerian-audit-ai/
├── data/
│   ├── raw/                    # Scraped data
│   ├── processed/              # Cleaned data
│   ├── training/               # Training datasets
│   └── regulations/            # Regulatory documents
├── models/
│   ├── saved_models/           # Trained models
│   ├── checkpoints/            # Training checkpoints
│   └── exports/                # Export-ready models
└── scripts/
    └── train_models.py         # Main training script
```

This guide covers the complete model training process for the Nigerian Audit AI system. The training script is designed to handle Nigerian-specific financial regulations and complian