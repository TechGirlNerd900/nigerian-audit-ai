#!/usr/bin/env python3
"""
Custom PDF Processing Script for Nigerian Audit AI

This script processes your custom PDF documents and prepares them for training.
"""

import os
import json
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.utils.document_parser import DocumentParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NigerianDocumentProcessor:
    """Enhanced processor for Nigerian financial documents"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.pdf_dir = Path("data/custom_pdfs")
        self.output_dir = Path("data/processed")
        self.output_dir.mkdir(exist_ok=True)
    
    def process_all_pdfs(self):
        """Process all PDFs in the custom_pdfs directory"""
        
        if not self.pdf_dir.exists():
            logger.info(f"Creating directory: {self.pdf_dir}")
            self.pdf_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Please add your PDF files to {self.pdf_dir}")
            return []
        
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.info(f"No PDF files found in {self.pdf_dir}")
            logger.info("Please add your PDF files to this directory and run again.")
            return []
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        processed_docs = []
        
        for pdf_file in pdf_files:
            logger.info(f"Processing {pdf_file.name}...")
            
            try:
                # Read PDF content
                with open(pdf_file, 'rb') as f:
                    pdf_content = f.read()
                
                # Extract text
                text = self.parser.parse_pdf(pdf_content)
                
                if not text.strip():
                    logger.warning(f"No text extracted from {pdf_file.name} - might be image-based PDF")
                    continue
                
                # Extract entities
                entities = self.extract_nigerian_entities(text)
                
                # Classify document
                doc_type = self.classify_document(pdf_file.name, text)
                
                # Extract financial data if applicable
                financial_data = self.extract_financial_data(text)
                
                processed_doc = {
                    'filename': pdf_file.name,
                    'text': text[:5000],  # Limit text length for storage
                    'full_text_length': len(text),
                    'entities': entities,
                    'document_type': doc_type,
                    'financial_data': financial_data,
                    'source': 'custom_pdf'
                }
                
                processed_docs.append(processed_doc)
                logger.info(f"✓ Processed {pdf_file.name} as {doc_type}")
                
            except Exception as e:
                logger.error(f"✗ Error processing {pdf_file.name}: {e}")
        
        # Save processed data
        output_file = self.output_dir / "custom_pdf_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_docs, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ Processed {len(processed_docs)} PDFs successfully")
        logger.info(f"Data saved to {output_file}")
        
        # Print summary
        self.print_summary(processed_docs)
        
        return processed_docs
    
    def extract_nigerian_entities(self, text: str) -> dict:
        """Extract Nigerian-specific entities from text"""
        
        import re
        entities = {}
        
        # Basic entities from parent class
        basic_entities = self.parser.extract_entities(text)
        entities.update(basic_entities)
        
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
        naira_patterns = [
            r'₦\s*([\d,]+\.?\d*)',
            r'N\s*([\d,]+\.?\d*)',
            r'NGN\s*([\d,]+\.?\d*)',
            r'Naira\s*([\d,]+\.?\d*)'
        ]
        
        amounts = []
        for pattern in naira_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amount = float(match.replace(',', ''))
                    amounts.append(amount)
                except ValueError:
                    continue
        
        if amounts:
            entities['naira_amounts'] = amounts[:10]  # Limit to first 10 amounts
        
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
                try:
                    entities[ratio_name] = float(match.group(1))
                except ValueError:
                    continue
        
        return entities
    
    def classify_document(self, filename: str, text: str) -> str:
        """Classify document type based on filename and content"""
        
        filename_lower = filename.lower()
        text_lower = text.lower()
        
        # Financial statements
        if any(word in filename_lower for word in ['financial', 'statement', 'balance', 'income']):
            return 'financial_statement'
        
        if any(phrase in text_lower for phrase in [
            'statement of financial position',
            'statement of comprehensive income',
            'statement of cash flows',
            'trial balance'
        ]):
            return 'financial_statement'
        
        # Audit reports
        if any(word in filename_lower for word in ['audit', 'report', 'opinion']):
            return 'audit_report'
        
        if any(phrase in text_lower for phrase in [
            'independent auditor',
            'audit opinion',
            'management letter',
            'auditor\'s report'
        ]):
            return 'audit_report'
        
        # Tax documents
        if any(word in filename_lower for word in ['tax', 'firs', 'vat']):
            return 'tax_document'
        
        if any(phrase in text_lower for phrase in [
            'company income tax',
            'value added tax',
            'withholding tax'
        ]):
            return 'tax_document'
        
        # Compliance documents
        if any(word in filename_lower for word in ['compliance', 'regulatory', 'frc']):
            return 'compliance_document'
        
        # Annual reports
        if any(word in filename_lower for word in ['annual', 'yearly']):
            return 'annual_report'
        
        return 'general_document'
    
    def extract_financial_data(self, text: str) -> dict:
        """Extract financial data for training"""
        
        import re
        financial_data = {}
        
        # Common financial statement items
        financial_items = {
            'revenue': [r'revenue[:\s]*([\d,]+)', r'sales[:\s]*([\d,]+)', r'turnover[:\s]*([\d,]+)'],
            'profit': [r'profit[:\s]*([\d,]+)', r'net income[:\s]*([\d,]+)'],
            'assets': [r'total assets[:\s]*([\d,]+)', r'assets[:\s]*([\d,]+)'],
            'liabilities': [r'total liabilities[:\s]*([\d,]+)', r'liabilities[:\s]*([\d,]+)'],
            'equity': [r'equity[:\s]*([\d,]+)', r'shareholders.{0,10}equity[:\s]*([\d,]+)']
        }
        
        for item_name, patterns in financial_items.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        amount = float(match.group(1).replace(',', ''))
                        financial_data[item_name] = amount
                        break
                    except ValueError:
                        continue
        
        return financial_data
    
    def print_summary(self, processed_docs: list):
        """Print processing summary"""
        
        if not processed_docs:
            return
        
        print("\n" + "="*50)
        print("PDF PROCESSING SUMMARY")
        print("="*50)
        
        # Document types
        doc_types = {}
        for doc in processed_docs:
            doc_type = doc['document_type']
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        print(f"Total documents processed: {len(processed_docs)}")
        print("\nDocument types:")
        for doc_type, count in doc_types.items():
            print(f"  - {doc_type}: {count}")
        
        # Entities found
        entities_found = set()
        for doc in processed_docs:
            entities_found.update(doc['entities'].keys())
        
        print(f"\nEntities extracted: {', '.join(sorted(entities_found))}")
        
        # Financial data
        financial_docs = [doc for doc in processed_docs if doc['financial_data']]
        print(f"Documents with financial data: {len(financial_docs)}")
        
        print("\n" + "="*50)
        print("Ready for training! Run:")
        print("poetry run python scripts/train_models.py --collect-data")
        print("="*50)

def main():
    """Main function"""
    
    print("🇳🇬 Nigerian Audit AI - Custom PDF Processor")
    print("=" * 50)
    
    processor = NigerianDocumentProcessor()
    processed_docs = processor.process_all_pdfs()
    
    if processed_docs:
        print(f"\n✅ Successfully processed {len(processed_docs)} PDF documents")
        print("Your PDFs are now ready to be included in model training!")
    else:
        print("\n📁 No PDFs found or processed.")
        print(f"Add your PDF files to: {processor.pdf_dir}")
        print("Then run this script again.")

if __name__ == "__main__":
    main()