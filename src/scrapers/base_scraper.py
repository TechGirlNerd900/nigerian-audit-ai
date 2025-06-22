import asyncio
import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all Nigerian regulatory scrapers"""
    
    def __init__(self, delay: int = 5):
        self.delay = delay  # Delay between requests in seconds
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_url(self, url: str, **kwargs) -> str:
        """Fetch content from URL with rate limiting"""
        
        if not self.session:
            raise RuntimeError("Scraper must be used as async context manager")
        
        try:
            # Rate limiting
            await asyncio.sleep(self.delay)
            
            async with self.session.get(url, **kwargs) as response:
                response.raise_for_status()
                content = await response.text()
                
                logger.info(f"Successfully fetched: {url}")
                return content
                
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise
    
    async def fetch_multiple_urls(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple URLs with proper rate limiting"""
        
        results = {}
        for url in urls:
            try:
                content = await self.fetch_url(url)
                results[url] = content
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
                results[url] = None
        
        return results
    
    @abstractmethod
    async def collect_data(self) -> Dict:
        """Abstract method for data collection - must be implemented by subclasses"""
        pass
    
    def save_data(self, data: Dict, filename: str):
        """Save collected data to file"""
        import json
        import os
        
        os.makedirs('data/raw', exist_ok=True)
        
        with open(f'data/raw/{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved data to data/raw/{filename}")
