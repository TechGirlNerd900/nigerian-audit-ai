# Path: src/scrapers/ngx_scraper.py

from bs4 import BeautifulSoup
import requests
from typing import Dict, Any, List, Optional, Union
from loguru import logger
from src.scrapers.base_scraper import BaseScraper
from src.config.sources import NigerianRegulatorySources

logger.add("file.log", rotation="500 MB")

class NGXScraper(BaseScraper):
    """
    Scrapes financial data and company information from the Nigerian Exchange Group (NGX) website.
    """

    def __init__(self):
        super().__init__(NigerianRegulatorySources.NGX_MAIN_PORTAL)
        logger.info("Initialized NGXScraper.")

    def scrape_listed_companies(self) -> Optional[List[Dict[str, str]]]:
        """
        Scrapes a list of currently listed companies on the NGX.
        This often involves navigating to a specific page listing companies.
        """
        listed_companies_url = f"{self.base_url}/exchange/listed-companies/" # Hypothetical path
        logger.info(f"Attempting to scrape listed companies from: {listed_companies_url}")

        html_content = self.get_html(listed_companies_url)
        if html_content:
            soup = BeautifulSoup(html_content, 'lxml')
            companies = []
            # This is a hypothetical selector. Inspect NGX site for actual table/list structure.
            # Example: find a table with class 'company-list-table' and iterate through rows
            company_table = soup.find('table', class_='company-list-table')
            if company_table:
                rows = company_table.find_all('tr')
                for row in rows[1:]: # Skip header row
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 2: # Assuming at least Symbol and Company Name
                        symbol = cols[0].get_text(strip=True)
                        name = cols[1].get_text(strip=True)
                        companies.append({"symbol": symbol, "name": name})
            else:
                logger.warning(f"Could not find company list table on {listed_companies_url}. Trying general links.")
                # Fallback: look for general links that might lead to company profiles
                for link in soup.find_all('a', href=True):
                    text = link.get_text(strip=True)
                    if len(text) > 3 and text.isupper() and len(text) < 10: # Heuristic for stock symbols
                        href = link['href']
                        full_url = requests.compat.urljoin(listed_companies_url, href)
                        companies.append({"symbol": text, "name": text, "url": full_url}) # Name might be symbol initially
            logger.info(f"Found {len(companies)} listed companies (or potential links).")
            return companies
        else:
            logger.error("Failed to retrieve HTML for NGX listed companies.")
            return None

    def scrape_company_financials(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Scrapes financial statements (e.g., annual reports, quarterly results) for a given company symbol.
        This would typically involve navigating to the company's profile page and then to its financial reports section.
        """
        company_profile_url = f"{self.base_url}/exchange/company-profile/{symbol}/" # Hypothetical path
        logger.info(f"Attempting to scrape financials for {symbol} from: {company_profile_url}")

        html_content = self.get_html(company_profile_url)
        if html_content:
            soup = BeautifulSoup(html_content, 'lxml')
            financial_data = {"symbol": symbol}
            # --- Placeholder for parsing logic ---
            # Look for sections like "Financial Highlights", "Annual Reports", "Quarterly Results"
            # This will require detailed inspection of NGX company profile pages.
            # Example: find a table with financial figures
            financial_table = soup.find('table', {'class': 'financial-summary'})
            if financial_table:
                # Parse table rows and columns to extract data like Revenue, Profit, Assets, etc.
                # This is highly dependent on the actual HTML structure.
                logger.info(f"Found financial summary table for {symbol}. Parsing...")
                # For demonstration, mock some data
                financial_data.update({
                    "revenue_2023": 1500000000,
                    "profit_2023": 250000000,
                    "total_assets_2023": 5000000000,
                    "report_date": "2024-03-31"
                })
            else:
                logger.warning(f"Could not find financial summary table for {symbol}. Manual inspection needed.")

            # Look for links to full annual reports (often PDFs)
            report_links = soup.find_all('a', text=lambda t: t and 'annual report' in t.lower(), href=True)
            if report_links:
                financial_data['annual_reports'] = [requests.compat.urljoin(company_profile_url, link['href']) for link in report_links]
                logger.info(f"Found {len(report_links)} annual report links for {symbol}.")
            else:
                financial_data['annual_reports'] = []
                logger.info(f"No annual report links found for {symbol}.")

            return financial_data
        else:
            logger.error(f"Failed to retrieve HTML for NGX company financials for {symbol}.")
            return None

    def scrape(self, mode: str = "listed_companies", symbol: Optional[str] = None) -> Union[List[Dict[str, str]], Dict[str, Any], None]:
        """
        Main scrape method for NGX.
        Args:
            mode (str): "listed_companies" to get a list, "company_financials" to get financials for a symbol.
            symbol (str, optional): Required if mode is "company_financials".
        """
        if mode == "listed_companies":
            return self.scrape_listed_companies()
        elif mode == "company_financials":
            if symbol:
                return self.scrape_company_financials(symbol)
            else:
                logger.error("Symbol is required for 'company_financials' mode.")
                return None
        else:
            logger.error(f"Invalid mode: {mode}. Use 'listed_companies' or 'company_financials'.")
            return None

# Example Usage:
if __name__ == "__main__":
    ngx_scraper = NGXScraper()

    print("Scraping NGX listed companies...")
    companies = ngx_scraper.scrape(mode="listed_companies")
    if companies:
        print(f"Found {len(companies)} companies. First 3:")
        for company in companies[:3]:
            print(f"  - {company.get('symbol', 'N/A')}: {company.get('name', 'N/A')}")

        # Try to scrape financials for a dummy symbol (e.g., 'ZENITHBANK' or 'DANGCEM')
        # Replace 'ZENITHBANK' with a real symbol for actual testing.
        dummy_symbol = 'ZENITHBANK'
        print(f"\nScraping financials for {dummy_symbol}...")
        financials = ngx_scraper.scrape(mode="company_financials", symbol=dummy_symbol)
        if financials:
            print(f"\nFinancials for {dummy_symbol} (Mock/Partial):")
            print(financials)
        else:
            print(f"\nFailed to scrape financials for {dummy_symbol}.")
    else:
        print("Failed to scrape NGX listed companies.")
