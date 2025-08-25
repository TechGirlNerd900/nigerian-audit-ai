import asyncio
import logging
from typing import List, Dict
from playwright.async_api import async_playwright, Playwright

logger = logging.getLogger(__name__)

class FRCScraper:
    """Scrape financial regulations from the Financial Reporting Council of Nigeria (FRC)"""
    
    FRC_URL = "https://www.financialreportingcouncil.gov.ng/"

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close()
        await self.playwright.stop()

    async def collect_data(self) -> List[Dict]:
        """Collect all available regulations and standards from the FRC website."""
        logger.info("Scraping FRC website for regulations...")
        await self.page.goto(self.FRC_URL + "publications/", wait_until="networkidle")

        links = await self.page.query_selector_all("a.elementor-button-link")
        doc_urls = []
        for link in links:
            href = await link.get_attribute("href")
            if href and (href.endswith(".pdf") or "document" in href):
                doc_urls.append(href)

        documents = []
        for url in doc_urls:
            try:
                async with self.page.context.new_page() as doc_page:
                    await doc_page.goto(url, wait_until="networkidle")
                    content = await doc_page.content()
                    title = await doc_page.title()
                    doc_type = "pdf" if url.endswith(".pdf") else "html"
                    documents.append({
                        "title": title,
                        "source": url,
                        "content": content,
                        "type": doc_type
                    })
            except Exception as e:
                logger.error(f"Failed to download {url}: {e}")

        return documents
