import logging
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Process and analyze Nigerian financial documents"""
    
    def __init__(self):
        self.supported_types = [
            'invoice', 'receipt', 'bank_statement', 
            'contract', 'purchase_order', 'payment_voucher'
        ]
    
    def process_document(self, content: bytes, filename: str, document_type: str = None) -> Dict:
        """Main document processing function"""
        
        try:
            # Detect document type if not provided
            if not document_type:
                document_type = self._detect_document_type(filename, content)
            
            # Extract text content
            text_content = self._extract_text(content, filename)
            
            # Process based on document type
            if document_type == 'invoice':
                extracted_data = self._process_invoice(text_content)
            elif document_type == 'receipt':
                extracted_data = self._process_receipt(text_content)
            elif document_type == 'bank_statement':
                extracted_data = self._process_bank_statement(text_content)
            elif document_type == 'contract':
                extracted_data = self._process_contract(text_content)
            else:
                extracted_data = self._process_generic_document(text_content)
            
            # Validate extracted data
            validation_results = self._validate_extracted_data(extracted_data, document_type)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(extracted_data, validation_results)
            
            return {
                'document_type': document_type,
                'filename': filename,
                'extracted_data': extracted_data,
                'validation': validation_results,
                'confidence_score': confidence_score,
                'processing_timestamp': datetime.utcnow().isoformat(),
                'text_length': len(text_content),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            return {
                'document_type': document_type or 'unknown',
                'filename': filename,
                'error': str(e),
                'success': False,
                'processing_timestamp': datetime.utcnow().isoformat()
            }
    
    def _detect_document_type(self, filename: str, content: bytes) -> str:
        """Detect document type from filename and content"""
        
        filename_lower = filename.lower()
        
        # Check filename patterns
        if any(word in filename_lower for word in ['invoice', 'inv']):
            return 'invoice'
        elif any(word in filename_lower for word in ['receipt', 'rcpt']):
            return 'receipt'
        elif any(word in filename_lower for word in ['statement', 'stmt', 'bank']):
            return 'bank_statement'
        elif any(word in filename_lower for word in ['contract', 'agreement']):
            return 'contract'
        elif any(word in filename_lower for word in ['po', 'purchase', 'order']):
            return 'purchase_order'
        
        # If no clear pattern, return generic
        return 'financial_document'
    
    def _extract_text(self, content: bytes, filename: str) -> str:
        """Extract text from document content"""
        
        try:
            # For PDF files
            if filename.lower().endswith('.pdf'):
                return self._extract_text_from_pdf(content)
            
            # For image files
            elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                return self._extract_text_from_image(content)
            
            # For text files
            elif filename.lower().endswith('.txt'):
                return content.decode('utf-8')
            
            # Default: try to decode as text
            else:
                return content.decode('utf-8')
                
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return ""
    
    def _extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content"""
        # Placeholder - would use PyPDF2 or pdfplumber
        # For now, return empty string
        return ""
    
    def _extract_text_from_image(self, content: bytes) -> str:
        """Extract text from image using OCR"""
        # Placeholder - would use Tesseract or Google Vision API
        # For now, return empty string
        return ""
    
    def _process_invoice(self, text: str) -> Dict:
        """Process invoice document"""
        
        extracted_data = {
            'document_type': 'invoice',
            'invoice_number': self._extract_invoice_number(text),
            'date': self._extract_date(text),
            'due_date': self._extract_due_date(text),
            'vendor_name': self._extract_vendor_name(text),
            'vendor_address': self._extract_address(text, 'vendor'),
            'customer_name': self._extract_customer_name(text),
            'customer_address': self._extract_address(text, 'customer'),
            'line_items': self._extract_line_items(text),
            'subtotal': self._extract_amount(text, 'subtotal'),
            'vat_amount': self._extract_amount(text, 'vat'),
            'total_amount': self._extract_amount(text, 'total'),
            'currency': self._extract_currency(text),
            'payment_terms': self._extract_payment_terms(text)
        }
        
        return extracted_data
    
    def _process_receipt(self, text: str) -> Dict:
        """Process receipt document"""
        
        extracted_data = {
            'document_type': 'receipt',
            'receipt_number': self._extract_receipt_number(text),
            'date': self._extract_date(text),
            'merchant_name': self._extract_merchant_name(text),
            'merchant_address': self._extract_address(text, 'merchant'),
            'items': self._extract_line_items(text),
            'subtotal': self._extract_amount(text, 'subtotal'),
            'vat_amount': self._extract_amount(text, 'vat'),
            'total_amount': self._extract_amount(text, 'total'),
            'payment_method': self._extract_payment_method(text),
            'currency': self._extract_currency(text)
        }
        
        return extracted_data
    
    def _process_bank_statement(self, text: str) -> Dict:
        """Process bank statement"""
        
        extracted_data = {
            'document_type': 'bank_statement',
            'account_number': self._extract_account_number(text),
            'account_name': self._extract_account_name(text),
            'statement_period': self._extract_statement_period(text),
            'opening_balance': self._extract_amount(text, 'opening'),
            'closing_balance': self._extract_amount(text, 'closing'),
            'transactions': self._extract_transactions(text),
            'bank_name': self._extract_bank_name(text),
            'currency': self._extract_currency(text)
        }
        
        return extracted_data
    
    def _process_contract(self, text: str) -> Dict:
        """Process contract document"""
        
        extracted_data = {
            'document_type': 'contract',
            'contract_number': self._extract_contract_number(text),
            'parties': self._extract_contract_parties(text),
            'effective_date': self._extract_date(text),
            'expiry_date': self._extract_expiry_date(text),
            'contract_value': self._extract_amount(text, 'value'),
            'payment_terms': self._extract_payment_terms(text),
            'currency': self._extract_currency(text),
            'key_clauses': self._extract_key_clauses(text)
        }
        
        return extracted_data
    
    def _process_generic_document(self, text: str) -> Dict:
        """Process generic financial document"""
        
        extracted_data = {
            'document_type': 'financial_document',
            'date': self._extract_date(text),
            'amounts': self._extract_all_amounts(text),
            'parties': self._extract_parties(text),
            'reference_numbers': self._extract_reference_numbers(text),
            'currency': self._extract_currency(text)
        }
        
        return extracted_data
    
    # Helper methods for data extraction
    def _extract_invoice_number(self, text: str) -> Optional[str]:
        """Extract invoice number"""
        patterns = [
            r'invoice\s*#?\s*:?\s*([A-Z0-9\-/]+)',
            r'inv\s*#?\s*:?\s*([A-Z0-9\-/]+)',
            r'#\s*([A-Z0-9\-/]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extract date from text"""
        patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
            r'(\d{1,2}\s+\w+\s+\d{4})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_amount(self, text: str, amount_type: str) -> Optional[float]:
        """Extract monetary amount"""
        
        # Nigerian Naira patterns
        patterns = [
            rf'{amount_type}[:\s]*₦?([0-9,]+\.?\d*)',
            rf'₦\s*([0-9,]+\.?\d*)',
            rf'NGN\s*([0-9,]+\.?\d*)',
            rf'([0-9,]+\.?\d*)\s*naira'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        
        return None
    
    def _extract_currency(self, text: str) -> str:
        """Extract currency from text"""
        
        if '₦' in text or 'NGN' in text.upper() or 'NAIRA' in text.upper():
            return 'NGN'
        elif '$' in text or 'USD' in text.upper():
            return 'USD'
        elif '€' in text or 'EUR' in text.upper():
            return 'EUR'
        elif '£' in text or 'GBP' in text.upper():
            return 'GBP'
        
        return 'NGN'  # Default to Naira for Nigerian documents
    
    def _extract_line_items(self, text: str) -> List[Dict]:
        """Extract line items from invoice/receipt"""
        
        # Simplified line item extraction
        lines = text.split('\n')
        items = []
        
        for line in lines:
            # Look for lines with quantity, description, and amount
            if re.search(r'\d+.*₦?\d+', line):
                items.append({
                    'description': line.strip(),
                    'amount': self._extract_amount(line, '')
                })
        
        return items[:10]  # Limit to 10 items
    
    def _extract_all_amounts(self, text: str) -> List[float]:
        """Extract all monetary amounts from text"""
        
        amounts = []
        patterns = [
            r'₦\s*([0-9,]+\.?\d*)',
            r'NGN\s*([0-9,]+\.?\d*)',
            r'([0-9,]+\.?\d*)\s*naira'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amount = float(match.replace(',', ''))
                    amounts.append(amount)
                except ValueError:
                    continue
        
        return sorted(set(amounts), reverse=True)[:10]  # Top 10 unique amounts
    
    def _validate_extracted_data(self, data: Dict, document_type: str) -> Dict:
        """Validate extracted data"""
        
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'required_fields_present': 0,
            'total_required_fields': 0
        }
        
        # Define required fields by document type
        required_fields = {
            'invoice': ['invoice_number', 'date', 'vendor_name', 'total_amount'],
            'receipt': ['receipt_number', 'date', 'merchant_name', 'total_amount'],
            'bank_statement': ['account_number', 'opening_balance', 'closing_balance'],
            'contract': ['parties', 'effective_date', 'contract_value']
        }
        
        required = required_fields.get(document_type, [])
        validation['total_required_fields'] = len(required)
        
        for field in required:
            if field in data and data[field] is not None:
                validation['required_fields_present'] += 1
            else:
                validation['errors'].append(f"Missing required field: {field}")
        
        # Validate amounts
        if 'total_amount' in data and data['total_amount']:
            if data['total_amount'] <= 0:
                validation['errors'].append("Total amount must be positive")
        
        # Validate dates
        if 'date' in data and data['date']:
            try:
                datetime.strptime(data['date'], '%Y-%m-%d')
            except ValueError:
                validation['warnings'].append("Date format may be incorrect")
        
        if validation['errors']:
            validation['is_valid'] = False
        
        return validation
    
    def _calculate_confidence_score(self, data: Dict, validation: Dict) -> float:
        """Calculate confidence score for extraction"""
        
        score = 100.0
        
        # Penalize for missing required fields
        if validation['total_required_fields'] > 0:
            completeness = validation['required_fields_present'] / validation['total_required_fields']
            score *= completeness
        
        # Penalize for validation errors
        if validation['errors']:
            score -= len(validation['errors']) * 20
        
        # Penalize for warnings
        if validation['warnings']:
            score -= len(validation['warnings']) * 5
        
        # Bonus for having amounts in Nigerian currency
        if data.get('currency') == 'NGN':
            score += 5
        
        return max(0, min(100, score))
    
    # Additional helper methods (simplified implementations)
    def _extract_due_date(self, text: str) -> Optional[str]:
        return self._extract_date(text)  # Simplified
    
    def _extract_vendor_name(self, text: str) -> Optional[str]:
        lines = text.split('\n')[:5]  # Check first 5 lines
        for line in lines:
            if len(line.strip()) > 5 and not re.search(r'\d', line):
                return line.strip()
        return None
    
    def _extract_customer_name(self, text: str) -> Optional[str]:
        return self._extract_vendor_name(text)  # Simplified
    
    def _extract_address(self, text: str, entity_type: str) -> Optional[str]:
        # Simplified address extraction
        return None
    
    def _extract_payment_terms(self, text: str) -> Optional[str]:
        patterns = [r'net\s+(\d+)', r'(\d+)\s+days']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def _extract_receipt_number(self, text: str) -> Optional[str]:
        return self._extract_invoice_number(text)  # Similar logic
    
    def _extract_merchant_name(self, text: str) -> Optional[str]:
        return self._extract_vendor_name(text)  # Similar logic
    
    def _extract_payment_method(self, text: str) -> Optional[str]:
        methods = ['cash', 'card', 'transfer', 'pos', 'mobile']
        for method in methods:
            if method in text.lower():
                return method.title()
        return None
    
    def _extract_account_number(self, text: str) -> Optional[str]:
        pattern = r'account.*?(\d{10})'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_account_name(self, text: str) -> Optional[str]:
        return None  # Would need more sophisticated extraction
    
    def _extract_statement_period(self, text: str) -> Optional[str]:
        return None  # Would extract date range
    
    def _extract_transactions(self, text: str) -> List[Dict]:
        return []  # Would extract transaction list
    
    def _extract_bank_name(self, text: str) -> Optional[str]:
        nigerian_banks = ['GTBank', 'Access', 'Zenith', 'UBA', 'First Bank', 'Fidelity']
        for bank in nigerian_banks:
            if bank.lower() in text.lower():
                return bank
        return None
    
    def _extract_contract_number(self, text: str) -> Optional[str]:
        return self._extract_invoice_number(text)  # Similar logic
    
    def _extract_contract_parties(self, text: str) -> List[str]:
        return []  # Would extract contracting parties
    
    def _extract_expiry_date(self, text: str) -> Optional[str]:
        return self._extract_date(text)  # Simplified
    
    def _extract_key_clauses(self, text: str) -> List[str]:
        return []  # Would extract important contract clauses
    
    def _extract_parties(self, text: str) -> List[str]:
        return []  # Generic party extraction
    
    def _extract_reference_numbers(self, text: str) -> List[str]:
        pattern = r'[A-Z]{2,}\d{4,}'
        return re.findall(pattern, text)