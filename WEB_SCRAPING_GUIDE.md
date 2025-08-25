# Nigerian Audit AI - Web Scraping Guide

This guide explains how to scrape real data from Nigerian financial sources to train your AI models with authentic regulatory and market data.

## Overview

The system includes specialized scrapers for:
- **NGX**: Nigerian Exchange (stock market data)
- **FRC**: Financial Reporting Council (regulations)
- **CAC**: Corporate Affairs Commission (company registrations)
- **FIRS**: Federal Inland Revenue Service (tax laws)
- **CBN**: Central Bank of Nigeria (banking regulations)

## Prerequisites

### Install Scraping Dependencies

```bash
# Install Playwright for dynamic content
poetry run playwright install

# Verify installation
poetry run playwright --version
```

### Environment Setup

No API keys required for basic scraping! The scrapers work with public data.

## Available Scrapers

### 1. NGX Scraper (Nigerian Exchange)

**What it scrapes:**
- All listed companies on the Nigerian Exchange
- Company financial statements
- Annual reports (PDF links)
- Market data

**Usage:**
```python
from src.scrapers.ngx_scraper import NGXScraper

ngx = NGXScraper()

# Get all listed companies
companies = ngx.scrape(mode="listed_companies")
print(f"Found {len(companies)} companies")

# Get specific company financials
financials = ngx.scrape(mode="company_financials", symbol="ZENITHBANK")
print(financials)
```

**Sample Output:**
```json
{
  "symbol": "ZENITHBANK",
  "revenue_2023": 1500000000,
  "profit_2023": 250000000,
  "total_assets_2023": 5000000000,
  "annual_reports": ["https://ngx.com/reports/zenith-2023.pdf"]
}
```

### 2. FRC Scraper (Financial Reporting Council)

**What it scrapes:**
- Regulatory documents (PDFs)
- Corporate governance guidelines
- Financial reporting standards
- Compliance requirements

**Usage:**
```python
import asyncio
from src.scrapers.frc_scraper import FRCScraper

async def scrape_frc():
    async with FRCScraper() as frc:
        documents = await frc.collect_data()
        print(f"Downloaded {len(documents)} regulatory documents")
        return documents

# Run the scraper
documents = asyncio.run(scrape_frc())
```

**Sample Output:**
```json
[
  {
    "title": "Nigerian Code of Corporate Governance 2018",
    "source": "https://frcnigeria.gov.ng/nccg-2018.pdf",
    "content": "PDF content...",
    "type": "pdf"
  }
]
```

### 3. CAC Scraper (Corporate Affairs Commission)

**What it scrapes:**
- Company registration details
- Director information
- Business addresses
- Registration status

**Usage:**
```python
from src.scrapers.cac_scraper import CACScraper

cac = CACScraper()
company_data = cac.scrape("RC123456")  # Registration number
print(company_data)
```

**Sample Output:**
```json
{
  "registration_number": "RC123456",
  "company_name": "Example Nigeria Limited",
  "status": "Active",
  "address": "Plot 123, Victoria Island, Lagos",
  "directors": ["John Doe", "Jane Smith"]
}
```

## Direct Document Downloads

The system also downloads key regulatory documents directly:

### Nigerian Legislation
- CAMA 2020 (Companies and Allied Matters Act)
- Finance Acts 2019-2023
- FIRS Transfer Pricing Regulations
- CBN Prudential Guidelines

### International Standards
- IFRS Standards (IAS 1, 2, 7, 8, 10, 12, 16, etc.)
- International Standards on Auditing
- Illustrative financial statements

## Running the Complete Scraping Pipeline

### Method 1: Integrated with Training

```bash
# Scrape data and train models in one command
poetry run python scripts/train_models.py --collect-data --epochs 100
```

### Method 2: Separate Data Collection

```bash
# First, collect all data
poetry run python scripts/collect_data.py

# Then train with collected data
poetry run python scripts/train_models.py
```

### Method 3: Manual Scraper Testing

```bash
# Test individual scrapers
poetry run python src/scrapers/ngx_scraper.py
poetry run python src/scrapers/cac_scraper.py

# Test async scrapers
poetry run python -c "
import asyncio
from src.scrapers.frc_scraper import FRCScraper

async def test():
    async with FRCScraper() as frc:
        docs = await frc.collect_data()
        print(f'Downloaded {len(docs)} documents')

asyncio.run(test())
"
```

## Data Processing Pipeline

### 1. Raw Data Collection
```
data/raw/
├── ngx_companies.json          # Listed companies
├── ngx_financials/             # Company financial data
├── frc_documents/              # Regulatory PDFs
├── cac_registrations.json      # Company registrations
└── regulatory_pdfs/            # Downloaded legislation
```

### 2. Data Processing
The `TrainingDataCollector` processes raw data into ML-ready formats:

```python
from src.training.data_collector import TrainingDataCollector

collector = TrainingDataCollector()
await collector.collect_all_data()  # Scrapes and processes
collector.prepare_training_datasets()  # Creates ML datasets
```

### 3. Training Data Output
```
data/training/
├── financial_analysis_dataset.csv
├── compliance_dataset.csv
├── risk_assessment_dataset.csv
├── trial_balance_classification_dataset.csv
└── document_intelligence_dataset.csv
```

## Troubleshooting

### Common Issues

**Playwright Installation:**
```bash
# If playwright fails to install
poetry run playwright install --with-deps

# For Ubuntu/Debian
sudo apt-get install libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxss1 libasound2
```

**Network Timeouts:**
```bash
# Increase timeout in scraper settings
# Edit src/scrapers/base_scraper.py
# Change: retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
```

**Website Structure Changes:**
If scrapers fail, the target websites may have changed their structure. Check:
1. `src/scrapers/` files for CSS selectors
2. Update selectors based on current website structure
3. Test with browser developer tools

### Debugging Scrapers

**Enable Debug Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run scraper with detailed logs
```

**Visual Debugging (Playwright):**
```python
# In CACScraper, change:
browser = p.chromium.launch(headless=False)  # Shows browser window
```

## Data Quality

### Validation
The system includes data validation:
- Financial ratios within reasonable ranges
- Company names and registration numbers format validation
- Document content verification
- Duplicate detection and removal

### Data Augmentation
Real scraped data is augmented with:
- Synthetic variations based on real patterns
- Historical data interpolation
- Cross-validation with multiple sources

## Legal and Ethical Considerations

### Compliance
- All scraped data is from public sources
- Respects robots.txt files
- Implements rate limiting to avoid overloading servers
- No personal or confidential data collection

### Usage Guidelines
- Use scraped data for training and research only
- Respect website terms of service
- Implement appropriate delays between requests
- Monitor for website policy changes

## Performance Optimization

### Concurrent Scraping
```python
import asyncio
from src.scrapers.frc_scraper import FRCScraper

async def scrape_multiple():
    tasks = []
    for i in range(5):  # Scrape 5 sources concurrently
        task = asyncio.create_task(scrape_source(i))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

### Caching
- Downloaded documents are cached locally
- Incremental updates only fetch new content
- Database storage for processed data

### Resource Management
- Memory-efficient streaming for large files
- Disk space monitoring
- Automatic cleanup of temporary files

## Next Steps

After scraping data:

1. **Verify Data Quality**: Check `data/processed/` for cleaned datasets
2. **Train Models**: Use `--collect-data` flag for training with real data
3. **Monitor Performance**: Compare model accuracy with synthetic vs. real data
4. **Schedule Updates**: Set up periodic scraping for fresh data

## Command Reference

```bash
# Complete data collection and training
poetry run python scripts/train_models.py --collect-data

# Data collection only
poetry run python scripts/collect_data.py

# Test individual scrapers
poetry run python src/scrapers/ngx_scraper.py
poetry run python -m src.scrapers.frc_scraper

# Debug mode with verbose logging
PYTHONPATH=. poetry run python scripts/collect_data.py --debug
```

This scraping system provides authentic Nigerian financial and regulatory data to train your AI models with real-world patterns and compliance requirements.