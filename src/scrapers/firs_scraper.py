# Path: src/scrapers/firs_scraper.py

from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
from loguru import logger
from src.scrapers.base_scraper import BaseScraper
from src.config.sources import NigerianRegulatorySources

logger.add("file.log", rotation="500 MB")

class FIRSScraper(BaseScraper):
    """
    Scrapes tax-related information and regulations from the Federal Inland Revenue Service (FIRS) portal.
    Note: FIRS portal might have dynamic content or specific APIs for tax lookup.
    This scraper focuses on general information and tax laws.
    """

    def __init__(self):
        super().__init__(NigerianRegulatorySources.FIRS_MAIN_PORTAL)
        logger.info("Initialized FIRSScraper.")

    def scrape_tax_laws_list(self) -> Optional[List[Dict[str, str]]]:
        """
        Scrapes a list of tax laws and their links from the FIRS tax laws section.
        """
        tax_laws_url = NigerianRegulatorySources.FIRS_TAX_LAWS
        logger.info(f"Attempting to scrape tax laws from: {tax_laws_url}")

        html_content = self.get_html(tax_laws_url)
        if html_content:
            soup = BeautifulSoup(html_content, 'lxml')
            tax_laws = []
            # This is a hypothetical selector. You need to inspect the FIRS tax laws page
            # to find the actual HTML structure (e.g., a list of links, table, etc.).
            # Example: find all <a> tags within a specific div/section that contain "Act" or "Regulation"
            law_links = soup.find_all('a', href=True) # Find all links
            for link in law_links:
                text = link.get_text(strip=True)
                href = link['href']
                # Filter for relevant links (e.g., containing 'Act', 'Regulation', 'Law', or specific keywords)
                if any(keyword in text.lower() for keyword in ['act', 'regulation', 'law', 'finance']):
                    # Construct full URL if it's relative
                    full_url = requests.compat.urljoin(tax_laws_url, href)
                    tax_laws.append({"title": text, "url": full_url})
            logger.info(f"Found {len(tax_laws)} potential tax law links.")
            return tax_laws
        else:
            logger.error("Failed to retrieve HTML for FIRS tax laws.")
            return None

    def scrape_tax_law_content(self, url: str) -> Optional[str]:
        """
        Fetches the full text content of a specific tax law document.
        Assumes the URL points to a readable HTML page or a downloadable PDF.
        For PDFs, you'd need a PDF parsing library (e.g., PyPDF2, pdfminer.six).
        """
        logger.info(f"Attempting to scrape content from tax law URL: {url}")
        # Check if it's a PDF
        if url.lower().endswith('.pdf'):
            logger.warning(f"PDF detected at {url}. PDF scraping not implemented yet. "
                           "Requires a PDF parsing library (e.g., PyPDF2, pdfminer.six).")
            # Placeholder for PDF handling
            # response = self._make_request(url, stream=True)
            # with open("temp_tax_law.pdf", "wb") as f:
            #     for chunk in response.iter_content(chunk_size=8192):
            #         f.write(chunk)
            # # Then parse PDF...
            return None
        else:
            html_content = self.get_html(url)
            if html_content:
                soup = BeautifulSoup(html_content, 'lxml')
                # Try to find the main content area (e.g., a div with article text)
                # These selectors are hypothetical, inspect the FIRS site.
                content_div = soup.find('div', class_='main-content') or soup.find('article')
                if content_div:
                    # Extract text, remove scripts/styles, clean up whitespace
                    for script_or_style in content_div(["script", "style"]):
                        script_or_style.extract()
                    text_content = content_div.get_text(separator='\n', strip=True)
                    logger.info(f"Successfully extracted text content from {url}.")
                    return text_content
                else:
                    logger.warning(f"Could not find main content div/article for {url}. Returning full text.")
                    return soup.get_text(separator='\n', strip=True) # Fallback to full text
            else:
                logger.error(f"Failed to retrieve HTML for tax law content from {url}.")
                return None

    def scrape(self, mode: str = "laws_list", url: Optional[str] = None) -> Union[List[Dict[str, str]], str, None]:
        """
        Main scrape method for FIRS.
        Args:
            mode (str): "laws_list" to get a list of tax laws, "law_content" to get content of a specific law.
            url (str, optional): Required if mode is "law_content".
        """
        if mode == "laws_list":
            return self.scrape_tax_laws_list()
        elif mode == "law_content":
            if url:
                return self.scrape_tax_law_content(url)
            else:
                logger.error("URL is required for 'law_content' mode.")
                return None
        else:
            logger.error(f"Invalid mode: {mode}. Use 'laws_list' or 'law_content'.")
            return None

# Example Usage:
if __name__ == "__main__":
    firs_scraper = FIRSScraper()

    print("Scraping FIRS tax laws list...")
    tax_laws = firs_scraper.scrape(mode="laws_list")
    if tax_laws:
        print(f"Found {len(tax_laws)} tax laws. First 3:")
        for law in tax_laws[:3]:
            print(f"  - {law['title']}: {law['url']}")

        # Try to scrape content of the first law (if available and not PDF)
        if tax_laws and not tax_laws[0]['url'].lower().endswith('.pdf'):
            first_law_content = firs_scraper.scrape(mode="law_content", url=tax_laws[0]['url'])
            if first_law_content:
                print(f"\nContent of first law (excerpt):\n{first_law_content[:500]}...")
            else:
                print("\nFailed to scrape content of the first law or it's a PDF.")
    else:
        print("Failed to scrape FIRS tax laws list.")
