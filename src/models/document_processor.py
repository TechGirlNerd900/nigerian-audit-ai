import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

# Correctly import the DocumentParser utility
from ..utils.document_parser import DocumentParser

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Processes and analyzes various Nigerian financial documents by extracting
    and structuring their content.
    """

    def __init__(self):
        """Initializes the DocumentProcessor."""
        self.supported_types = [
            'invoice', 'receipt', 'bank_statement',
            'contract', 'purchase_order', 'payment_voucher'
        ]

    def process_document(self, content: bytes, filename: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Main document processing function. It orchestrates the detection,
        text extraction, and data processing for a given document.

        Args:
            content: The byte content of the document file.
            filename: The name of the document file.
            document_type: The optional type of the document.

        Returns:
            A dictionary containing the extracted data and processing metadata.
        """
        try:
            # 1. Detect document type if not provided
            if not document_type:
                document_type = self._detect_document_type(filename, content)

            # 2. Extract text content using the utility
            text_content = self._extract_text(content, filename)
            if not text_content:
                raise ValueError("Failed to extract any text from the document.")

            # 3. Process based on document type
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

            # 4. Validate extracted data
            validation_results = self._validate_extracted_data(extracted_data, document_type)

            # 5. Calculate confidence score
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
            logger.error(f"Document processing failed for {filename}: {e}")
            return {
                'document_type': document_type or 'unknown',
                'filename': filename,
                'error': str(e),
                'success': False,
                'processing_timestamp': datetime.utcnow().isoformat()
            }

    def _detect_document_type(self, filename: str, content: bytes) -> str:
        """Detects document type from filename and content."""
        filename_lower = filename.lower()
        if any(word in filename_lower for word in ['invoice', 'inv']):
            return 'invoice'
        if any(word in filename_lower for word in ['receipt', 'rcpt']):
            return 'receipt'
        if any(word in filename_lower for word in ['statement', 'stmt', 'bank']):
            return 'bank_statement'
        if any(word in filename_lower for word in ['contract', 'agreement']):
            return 'contract'
        if any(word in filename_lower for word in ['po', 'purchase', 'order']):
            return 'purchase_order'
        return 'financial_document'

    def _extract_text(self, content: bytes, filename: str) -> str:
        """
        Extracts text from document content by delegating to the DocumentParser.
        This method replaces the old placeholder logic.
        """
        try:
            return DocumentParser.extract_text(content, filename)
        except Exception as e:
            logger.error(f"Text extraction failed via DocumentParser: {e}")
            return ""

    # --------------------------------------------------------------------------
    # PROCESSING LOGIC FOR SPECIFIC DOCUMENT TYPES
    # --------------------------------------------------------------------------

    def _process_invoice(self, text: str) -> Dict[str, Any]:
        """Processes an invoice document."""
        return {
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

    def _process_receipt(self, text: str) -> Dict[str, Any]:
        """Processes a receipt document."""
        return {
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

    def _process_bank_statement(self, text: str) -> Dict[str, Any]:
        """Processes a bank statement."""
        return {
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

    def _process_contract(self, text: str) -> Dict[str, Any]:
        """Processes a contract document."""
        return {
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

    def _process_generic_document(self, text: str) -> Dict[str, Any]:
        """Processes a generic financial document."""
        return {
            'document_type': 'financial_document',
            'date': self._extract_date(text),
            'amounts': self._extract_all_amounts(text),
            'parties': self._extract_parties(text),
            'reference_numbers': self._extract_reference_numbers(text),
            'currency': self._extract_currency(text)
        }

    # --------------------------------------------------------------------------
    # HELPER METHODS FOR DATA EXTRACTION (using regex)
    # --------------------------------------------------------------------------

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        patterns = [r'invoice\s*#?\s*:?\s*([A-Z0-9\-/]+)', r'inv\s*#?\s*:?\s*([A-Z0-9\-/]+)', r'#\s*([A-Z0-9\-/]+)']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_date(self, text: str) -> Optional[str]:
        patterns = [r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})', r'(\d{1,2}\s+\w+\s+\d{4})']
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None

    def _extract_amount(self, text: str, amount_type: str) -> Optional[float]:
        # Improved regex to handle various amount contexts
        patterns = [
            rf'{amount_type}[\s:]*₦?([0-9,]+\.?\d{{2}}?)',
            rf'{amount_type}[\s:]*NGN\s?([0-9,]+\.?\d{{2}}?)',
        ]
        if amount_type.lower() == 'total':
             patterns.append(r'Total[\s:]*₦?([0-9,]+\.?\d{2})')

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
        if '₦' in text or 'NGN' in text.upper() or 'NAIRA' in text.upper():
            return 'NGN'
        if '$' in text or 'USD' in text.upper():
            return 'USD'
        return 'NGN'  # Default to Naira

    def _extract_line_items(self, text: str) -> List[Dict[str, Any]]:
        items = []
        # A simple pattern looking for lines with a description and an amount
        pattern = re.compile(r'^(.*?)[\s\t]+(₦?[\d,]+\.\d{2})$', re.MULTILINE)
        matches = pattern.findall(text)
        for desc, amt_str in matches:
            if len(desc.strip()) > 3: # Basic check for a real description
                try:
                    amount = float(amt_str.replace('₦', '').replace(',', ''))
                    items.append({'description': desc.strip(), 'amount': amount})
                except ValueError:
                    continue
        return items[:15] # Limit number of items

    def _extract_all_amounts(self, text: str) -> List[float]:
        amounts = []
        patterns = [r'₦\s*([0-9,]+\.?\d*)', r'NGN\s*([0-9,]+\.?\d*)']
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amounts.append(float(match.replace(',', '')))
                except ValueError:
                    continue
        return sorted(list(set(amounts)), reverse=True)[:10]

    def _extract_vendor_name(self, text: str) -> Optional[str]:
        # Look for a line near the top that looks like a company name
        for line in text.split('\n')[:5]:
            # Simple heuristic: often contains Ltd, Limited, PLC, or is in all caps
            if re.search(r'\b(LTD|LIMITED|PLC|INC)\b', line, re.IGNORECASE) or line.isupper():
                return line.strip()
        return None
    
    # ... Other specific extraction helpers would be implemented here ...
    # These are simplified placeholders for now.
    def _extract_due_date(self, text: str) -> Optional[str]: return self._extract_date(text)
    def _extract_customer_name(self, text: str) -> Optional[str]: return None
    def _extract_address(self, text: str, entity_type: str) -> Optional[str]: return None
    def _extract_payment_terms(self, text: str) -> Optional[str]: return None
    def _extract_receipt_number(self, text: str) -> Optional[str]: return self._extract_invoice_number(text)
    def _extract_merchant_name(self, text: str) -> Optional[str]: return self._extract_vendor_name(text)
    def _extract_payment_method(self, text: str) -> Optional[str]: return None
    def _extract_account_number(self, text: str) -> Optional[str]:
        match = re.search(r'account\s+number\s*[:\-]?\s*(\d{10})', text, re.I)
        return match.group(1) if match else None
    def _extract_account_name(self, text: str) -> Optional[str]: return None
    def _extract_statement_period(self, text: str) -> Optional[str]: return None
    def _extract_transactions(self, text: str) -> List[Dict]: return []
    def _extract_bank_name(self, text: str) -> Optional[str]: return None
    def _extract_contract_number(self, text: str) -> Optional[str]: return None
    def _extract_contract_parties(self, text: str) -> List[str]: return []
    def _extract_expiry_date(self, text: str) -> Optional[str]: return None
    def _extract_key_clauses(self, text: str) -> List[str]: return []
    def _extract_parties(self, text: str) -> List[str]: return []
    def _extract_reference_numbers(self, text: str) -> List[str]: return []


    # --------------------------------------------------------------------------
    # VALIDATION AND CONFIDENCE SCORING
    # --------------------------------------------------------------------------

    def _validate_extracted_data(self, data: Dict, document_type: str) -> Dict[str, Any]:
        """Validates the extracted data based on document type."""
        validation = {'is_valid': True, 'errors': [], 'warnings': []}
        required_fields = {
            'invoice': ['invoice_number', 'date', 'total_amount'],
            'receipt': ['date', 'total_amount'],
            'bank_statement': ['account_number', 'closing_balance'],
        }
        fields_to_check = required_fields.get(document_type, [])
        for field in fields_to_check:
            if not data.get(field):
                validation['errors'].append(f"Missing required field: {field}")

        if validation['errors']:
            validation['is_valid'] = False
        return validation

    def _calculate_confidence_score(self, data: Dict[str, Any], validation: Dict[str, Any]) -> float:
        """Calculates a confidence score for the extraction process."""
        score = 100.0
        
        # Penalize for validation errors
        score -= len(validation.get('errors', [])) * 25.0
        
        # Check for key fields
        if not data.get('total_amount'):
            score -= 20.0
        if not data.get('date'):
            score -= 10.0
        if data.get('currency') != 'NGN':
            score -= 5.0 # Slight penalty if not in local currency
        
        return max(0.0, min(100.0, score))

