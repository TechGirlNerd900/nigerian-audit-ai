import io
import re
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import pytesseract
from PIL import Image

class DocumentParser:
    def parse_pdf(self, content: bytes) -> str:
        """Extract text from PDF content."""
        return extract_text(io.BytesIO(content))

    def parse_html(self, content: str) -> str:
        """Extract text from HTML content."""
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()

    def parse_image(self, content: bytes) -> str:
        """Extract text from image content using OCR."""
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

    def extract_entities(self, text: str) -> dict:
        """Extract entities from text using regex."""
        
        entities = {}
        
        # Regex for invoice number
        invoice_number_pattern = r'Invoice No[:\s]*(\w+)'
        match = re.search(invoice_number_pattern, text, re.IGNORECASE)
        if match:
            entities['invoice_number'] = match.group(1)
            
        # Regex for date
        date_pattern = r'Date[:\s]*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        match = re.search(date_pattern, text, re.IGNORECASE)
        if match:
            entities['date'] = match.group(1)
            
        # Regex for total amount
        total_amount_pattern = r'Total Amount[:\s]*(\d{1,3}(?:,\d{3})*\.\d{2})'
        match = re.search(total_amount_pattern, text, re.IGNORECASE)
        if match:
            entities['total_amount'] = float(match.group(1).replace(',', ''))
            
        return entities
