# Path: src/scrapers/base_scraper.py

import requests
from requests.exceptions import RequestException, Timeout, HTTPError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from loguru import logger
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger.add("file.log", rotation="500 MB")

class BaseScraper(ABC):
    """
    Abstract base class for all web scrapers.
    Provides common functionalities like robust HTTP requests with retries.
    """

    def __init__(self, base_url: str, retries: int = 3, delay: int = 2):
        """
        Initializes the BaseScraper.

        Args:
            base_url (str): The base URL for the scraper.
            retries (int): Number of times to retry a failed request.
            delay (int): Delay in seconds between retries.
        """
        self.base_url = base_url
        self.retries = retries
        self.delay = delay
        self.session = requests.Session() # Use a session for connection pooling
        logger.info(f"Initialized BaseScraper for {base_url} with {retries} retries.")

    @retry(
        stop=stop_after_attempt(3), # Max 3 attempts
        wait=wait_fixed(2),        # Wait 2 seconds between attempts
        retry=retry_if_exception_type((RequestException, Timeout, HTTPError)),
        reraise=True # Re-raise the last exception if all retries fail
    )
    def _make_request(self, url: str, method: str = 'GET', **kwargs) -> requests.Response:
        """
        Makes an HTTP request with retry logic.

        Args:
            url (str): The URL to request.
            method (str): HTTP method (GET, POST, etc.).
            **kwargs: Additional keyword arguments for requests.request().

        Returns:
            requests.Response: The response object.

        Raises:
            RequestException: If the request fails after all retries.
        """
        try:
            logger.debug(f"Making {method} request to: {url}")
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            logger.info(f"Successfully fetched data from {url}")
            return response
        except Timeout:
            logger.error(f"Request to {url} timed out.")
            raise
        except HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e.response.text}")
            raise
        except RequestException as e:
            logger.error(f"Network or request error for {url}: {e}")
            raise

    def get_html(self, url: str, **kwargs) -> Optional[str]:
        """
        Fetches HTML content from a given URL.

        Args:
            url (str): The URL to fetch.
            **kwargs: Additional keyword arguments for requests.get().

        Returns:
            Optional[str]: The HTML content as a string, or None if an error occurred.
        """
        try:
            response = self._make_request(url, method='GET', **kwargs)
            return response.text
        except RequestException:
            logger.error(f"Failed to get HTML from {url} after retries.")
            return None

    def post_json(self, url: str, data: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
        """
        Sends JSON data to a URL and expects a JSON response.

        Args:
            url (str): The URL to post to.
            data (Dict[str, Any]): The JSON data to send.
            **kwargs: Additional keyword arguments for requests.post().

        Returns:
            Optional[Dict[str, Any]]: The JSON response as a dictionary, or None if an error occurred.
        """
        try:
            response = self._make_request(url, method='POST', json=data, **kwargs)
            return response.json()
        except RequestException:
            logger.error(f"Failed to post JSON to {url} after retries.")
            return None
        except ValueError: # If response is not valid JSON
            logger.error(f"Received non-JSON response from {url}.")
            return None

    @abstractmethod
    def scrape(self, *args, **kwargs) -> Any:
        """
        Abstract method to be implemented by concrete scraper classes.
        This method should contain the specific logic for scraping data.
        """
        pass

# Example Usage (for demonstration, not part of the actual file)
if __name__ == "__main__":
    class DummyScraper(BaseScraper):
        def __init__(self):
            super().__init__("http://httpbin.org")

        def scrape(self, endpoint: str):
            logger.info(f"Scraping dummy endpoint: {endpoint}")
            return self.get_html(f"{self.base_url}/{endpoint}")

    scraper = DummyScraper()
    print("Trying to fetch /status/200...")
    content = scraper.scrape("status/200")
    if content:
        print("Successfully fetched content.")
    else:
        print("Failed to fetch content.")

    print("\nTrying to fetch /status/500 (will retry)...")
    content = scraper.scrape("status/500") # This will fail after retries
    if content:
        print("Successfully fetched content.")
    else:
        print("Failed to fetch content after retries (expected).")
