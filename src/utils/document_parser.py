import logging
from typing import Dict, List, Any, Optional
import io
from PIL import Image
import pytesseract
from pdfplumber import open as open_pdf

logger = logging.getLogger(__name__)

class DocumentParser:
    """A utility class to extract text from various document types."""

    @staticmethod
    def extract_text_from_pdf(content: bytes) -> str:
        """
        Extracts text from the content of a PDF file.

        Args:
            content: The byte content of the PDF file.

        Returns:
            The extracted text as a single string.
        """
        text = ""
        try:
            with open_pdf(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            logger.info("Successfully extracted text from PDF.")
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            return ""

    @staticmethod
    def extract_text_from_image(content: bytes) -> str:
        """
        Extracts text from the content of an image file using Tesseract OCR.

        Args:
            content: The byte content of the image file.

        Returns:
            The extracted text.
        """
        try:
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image, lang='eng')
            logger.info("Successfully extracted text from image.")
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from image: {e}")
            return ""

    @staticmethod
    def extract_text(content: bytes, filename: str) -> str:
        """
        Extracts text from a document based on its file extension.

        Args:
            content: The byte content of the file.
            filename: The name of the file, including its extension.

        Returns:
            The extracted text.
        """
        filename_lower = filename.lower()
        if filename_lower.endswith('.pdf'):
            return DocumentParser.extract_text_from_pdf(content)
        elif filename_lower.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            return DocumentParser.extract_text_from_image(content)
        elif filename_lower.endswith('.txt'):
            return content.decode('utf-8')
        else:
            try:
                # Attempt to decode as text as a fallback
                return content.decode('utf-8')
            except UnicodeDecodeError:
                logger.warning(f"Could not decode file as text: {filename}")
                return ""