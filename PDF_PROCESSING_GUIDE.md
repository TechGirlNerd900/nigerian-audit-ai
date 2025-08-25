# PDF Processing Guide for Nigerian Audit AI

This guide shows you how to add your own PDF documents to train the AI models with your specific data.

## Current PDF Processing Capabilities

The project includes a `DocumentParser` class that can:
- **Extract text from PDFs** using `pdfminer`
- **Parse HTML documents** 
- **OCR image-based PDFs** using `pytesseract`
- **Extract entities** (invoice numbers, dates, amounts) using regex

## Adding Your Own PDFs

### Step 1: Prepare Your PDF Directory

Create a directory for your PDFs:

```bash
mkdir -p data/custom_pdfs
```

### Step 2: Add Your PDFs

Copy your PDF files to the directory:

```bash
# Example: Copy your audit reports, financial statements, etc.
cp /path/to/your/pdfs/*.pdf data/custom_pdfs/
```

### Step 3: Create a Custom PDF Processor

Create a script to process your PDFs:

```python
# scripts/process_custom_pdfs.py
import os
import json
from pathlib import Path
from src.utils.document_parser import DocumentParser

def process_custom_pdfs():
    """Process custom PDFs and extract training data"""
    
    pdf_dir = Path("data/custom_pdfs")
    output_dir = Path("data/processed")
    output_dir.mkdir(exist_ok=True)
    
    parser = DocumentParser()
    processed_docs = []
    
    # Process each PDF
    for pdf_file in pdf_dir.glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")
        
        try:
            # Read PDF content
            with open(pdf_file, 'rb') as f:
                pdf_content = f.read()
            
            # Extract text
            text = parser.parse_pdf(pdf_content)
            
            # Extract entities (amounts, dates, etc.)
            entities = parser.extract_entities(text)
            
            # Classify document type based on filename or content
            doc_type = classify_document(pdf_file.name, text)
            
            processed_doc = {
                'filename': pdf_file.name,
                'text': text,
                'entities': entities,
                'document_type': doc_type,
                'source': 'custom_pdf'
            }
            
            processed_docs.append(processed_doc)
            
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
    
    # Save processed data
    output_file = output_dir / "custom_pdf_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_docs, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(processed_docs)} PDFs")
    print(f"Data saved to {output_file}")
    
    return processed_docs

def classify_document(filename, text):
    """Classify document type based on filename and content"""
    
    filename_lower = filename.lower()
    text_lower = text.lower()
    
    # Financial statements
    if any(word in filename_lower for word in ['financial', 'statement', 'balance', 'income']):
        return 'financial_statement'
    
    # Audit reports
    if any(word in filename_lower for word in ['audit', 'report', 'opinion']):
        return 'audit_report'
    
    # Tax documents
    if any(word in filename_lower for word in ['tax', 'firs', 'vat']):
        return 'tax_document'
    
    # Compliance documents
    if any(word in filename_lower for word in ['compliance', 'regulatory', 'frc']):
        return 'compliance_document'
    
    # Check content for classification
    if any(word in text_lower for word in ['trial balance', 'debit', 'credit']):
        return 'trial_balance'
    
    if any(word in text_lower for word in ['revenue', 'profit', 'assets', 'liabilities']):
        return 'financial_statement'
    
    return 'general_document'

if __name__ == "__main__":
    process_custom_pdfs()
```

### Step 4: Run PDF Processing

```bash
# Create the processing script
poetry run python scripts/process_custom_pdfs.py
```

### Step 5: Integrate with Training Data

Modify the `TrainingDataCollector` to include your PDF data:

```python
# Add this method to src/training/data_collector.py

def collect_custom_pdf_data(self) -> List[Dict]:
    """Collect data from custom PDFs"""
    
    custom_pdf_file = os.path.join(self.processed_dir, "custom_pdf_data.json")
    
    if os.path.exists(custom_pdf_file):
        with open(custom_pdf_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        logger.warning("No custom PDF data found. Run process_custom_pdfs.py first.")
        return []

# Update the collect_all_data method to include custom PDFs
async def collect_all_data(self):
    """Collect all training data from various sources"""
    
    logger.info("Starting comprehensive training data collection...")
    
    # Existing scrapers...
    await self._collect_from_scrapers()
    await self.collect_regulatory_documents()
    
    # Add custom PDF processing
    custom_pdf_data = self.collect_custom_pdf_data()
    if custom_pdf_data:
        self._save_data(custom_pdf_data, "custom_pdf_training_data.json")
        logger.info(f"Loaded {len(custom_pdf_data)} custom PDF documents")
    
    # Continue with synthetic data...
    self._generate_synthetic_data()
    self.prepare_training_datasets()
    
    logger.info("Training data collection completed")
```

## Advanced PDF Processing

### Enhanced Entity Extraction

Extend the `DocumentParser` for Nigerian financial documents:

```python
# Enhanced version for src/utils/document_parser.py

import re
from typing import Dict, List

class NigerianDocumentParser(DocumentParser):
    """Enhanced parser for Nigerian financial documents"""
    
    def extract_nigerian_entities(self, text: str) -> Dict:
        """Extract Nigerian-specific entities"""
        
        entities = {}
        
        # Nigerian company registration numbers
        rc_pattern = r'RC[:\s]*(\d+)'
        match = re.search(rc_pattern, text, re.IGNORECASE)
        if match:
            entities['rc_number'] = match.group(1)
        
        # Tax Identification Numbers
        tin_pattern = r'TIN[:\s]*(\d{12})'
        match = re.search(tin_pattern, text, re.IGNORECASE)
        if match:
            entities['tin_number'] = match.group(1)
        
        # Nigerian Naira amounts
        naira_pattern = r'₦\s*([\d,]+\.?\d*)|N\s*([\d,]+\.?\d*)'
        matches = re.findall(naira_pattern, text)
        if matches:
            amounts = []
            for match in matches:
                amount = match[0] or match[1]
                amounts.append(float(amount.replace(',', '')))
            entities['naira_amounts'] = amounts
        
        # Financial ratios
        ratio_patterns = {
            'current_ratio': r'current ratio[:\s]*([\d.]+)',
            'debt_equity_ratio': r'debt.{0,10}equity ratio[:\s]*([\d.]+)',
            'profit_margin': r'profit margin[:\s]*([\d.]+)%?',
            'return_on_assets': r'return on assets[:\s]*([\d.]+)%?'
        }
        
        for ratio_name, pattern in ratio_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities[ratio_name] = float(match.group(1))
        
        # Nigerian regulatory references
        regulatory_refs = []
        reg_patterns = [
            r'CAMA\s*\d{4}',
            r'Finance Act\s*\d{4}',
            r'FRC[:\s]*\w+',
            r'FIRS[:\s]*\w+',
            r'CBN[:\s]*\w+'
        ]
        
        for pattern in reg_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            regulatory_refs.extend(matches)
        
        if regulatory_refs:
            entities['regulatory_references'] = regulatory_refs
        
        return entities
    
    def classify_nigerian_document(self, text: str) -> str:
        """Classify Nigerian financial documents"""
        
        text_lower = text.lower()
        
        # Financial statements
        if any(phrase in text_lower for phrase in [
            'statement of financial position',
            'statement of comprehensive income',
            'statement of cash flows',
            'statement of changes in equity'
        ]):
            return 'financial_statement'
        
        # Audit reports
        if any(phrase in text_lower for phrase in [
            'independent auditor',
            'audit opinion',
            'management letter',
            'auditor\'s report'
        ]):
            return 'audit_report'
        
        # Tax documents
        if any(phrase in text_lower for phrase in [
            'company income tax',
            'value added tax',
            'withholding tax',
            'firs assessment'
        ]):
            return 'tax_document'
        
        # Regulatory filings
        if any(phrase in text_lower for phrase in [
            'annual return',
            'statutory audit',
            'regulatory filing',
            'compliance report'
        ]):
            return 'regulatory_filing'
        
        return 'general_document'
```

### OCR for Scanned PDFs

For image-based PDFs (scanned documents):

```python
def process_scanned_pdfs():
    """Process scanned PDFs using OCR"""
    
    from PIL import Image
    import pytesseract
    import pdf2image
    
    pdf_dir = Path("data/custom_pdfs")
    parser = NigerianDocumentParser()
    
    for pdf_file in pdf_dir.glob("*.pdf"):
        try:
            # Convert PDF to images
            images = pdf2image.convert_from_path(pdf_file)
            
            full_text = ""
            for image in images:
                # OCR each page
                text = pytesseract.image_to_string(image)
                full_text += text + "\n"
            
            # Process extracted text
            entities = parser.extract_nigerian_entities(full_text)
            doc_type = parser.classify_nigerian_document(full_text)
            
            print(f"OCR processed {pdf_file.name}: {doc_type}")
            
        except Exception as e:
            print(f"OCR failed for {pdf_file.name}: {e}")
```

## Current Model Status

**No pre-trained models exist yet.** The project structure is ready but you need to train models first:

```bash
# Check current model status
ls -la models/saved_models/  # Empty directory

# Train models (this will create the models)
poetry run python scripts/train_models.py

# After training, you'll have:
# models/saved_models/financial_analysis.h5
# models/saved_models/compliance.h5
# models/saved_models/trial_balance_classification.h5
# models/saved_models/document_intelligence.h5
```

## Integration Workflow

### Complete PDF-to-Training Pipeline

```bash
# 1. Add your PDFs
cp your_pdfs/*.pdf data/custom_pdfs/

# 2. Process PDFs
poetry run python scripts/process_custom_pdfs.py

# 3. Train models with your PDF data
poetry run python scripts/train_models.py --collect-data

# 4. Your PDFs are now part of the training data!
```

### Training Data Sources After Adding PDFs

Your models will be trained on:
- **Your custom PDFs** (financial statements, audit reports, etc.)
- **Scraped Nigerian regulatory data** (FRC, NGX, CAC)
- **Synthetic data** (generated patterns)
- **International standards** (IFRS, auditing standards)

## Example Use Cases

### Audit Firm PDFs
```
data/custom_pdfs/
├── client_financial_statements_2023.pdf
├── audit_opinion_manufacturing_co.pdf
├── management_letter_bank_audit.pdf
└── tax_compliance_report.pdf
```

### Regulatory Documents
```
data/custom_pdfs/
├── cbn_circular_2024.pdf
├── frc_guidance_note.pdf
├── firs_tax_ruling.pdf
└── sec_market_bulletin.pdf
```

### Company Documents
```
data/custom_pdfs/
├── annual_report_2023.pdf
├── quarterly_results_q4.pdf
├── board_resolution.pdf
└── compliance_certificate.pdf
```

Each PDF type will be processed and classified automatically, then used to train the appropriate AI models for Nigerian audit and compliance tasks.