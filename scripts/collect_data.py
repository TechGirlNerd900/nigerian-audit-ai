"""
Nigerian Audit AI - Data Collection Script
Collect training data from various Nigerian sources
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.scrapers.ngx_scraper import NGXScraper
from src.scrapers.frc_scraper import FRCScraper
from src.scrapers.regulatory_updater import RegulatoryUpdater
from src.training.data_collector import TrainingDataCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🇳🇬 Starting Nigerian Financial Data Collection")
    
    try:
        # Initialize scrapers
        ngx_scraper = NGXScraper()
        frc_scraper = FRCScraper()
        regulatory_updater = RegulatoryUpdater()
        data_collector = TrainingDataCollector()
        
        # Collect data from different sources
        logger.info("📈 Collecting NGX financial statements...")
        await ngx_scraper.collect_annual_reports()
        
        logger.info("📋 Collecting FRC regulations...")
        await frc_scraper.collect_regulations()
        
        logger.info("🏛️ Updating regulatory data...")
        await regulatory_updater.update_all_regulations()
        
        logger.info("🤖 Preparing ML training data...")
        data_collector.prepare_training_datasets()
        
        logger.info("✅ Data collection completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Data collection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())