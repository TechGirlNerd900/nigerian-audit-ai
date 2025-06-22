import asyncio
import logging
from typing import Dict, List
from datetime import datetime, timedelta
from .frc_scraper import FRCScraper
from .ngx_scraper import NGXScraper

logger = logging.getLogger(__name__)

class RegulatoryUpdater:
    """Updates regulatory data from multiple Nigerian sources"""
    
    def __init__(self):
        self.scrapers = {
            'frc': FRCScraper(),
            'ngx': NGXScraper()
        }
        self.last_update = {}
    
    async def update_all_regulations(self) -> Dict:
        """Update all regulatory data"""
        
        logger.info("Starting comprehensive regulatory data update...")
        
        update_results = {
            'update_timestamp': datetime.now().isoformat(),
            'sources_updated': [],
            'failed_sources': [],
            'summary': {}
        }
        
        # Update each source
        for source_name, scraper in self.scrapers.items():
            try:
                logger.info(f"Updating {source_name} data...")
                
                data = await scraper.collect_data()
                
                if 'error' not in data:
                    update_results['sources_updated'].append(source_name)
                    update_results['summary'][source_name] = {
                        'status': 'success',
                        'records_collected': self._count_records(data),
                        'last_updated': datetime.now().isoformat()
                    }
                    self.last_update[source_name] = datetime.now()
                else:
                    update_results['failed_sources'].append(source_name)
                    update_results['summary'][source_name] = {
                        'status': 'failed',
                        'error': data['error'],
                        'last_attempted': datetime.now().isoformat()
                    }
                
            except Exception as e:
                logger.error(f"Failed to update {source_name}: {e}")
                update_results['failed_sources'].append(source_name)
                update_results['summary'][source_name] = {
                    'status': 'failed',
                    'error': str(e),
                    'last_attempted': datetime.now().isoformat()
                }
        
        # Generate update summary
        update_results['total_sources'] = len(self.scrapers)
        update_results['successful_updates'] = len(update_results['sources_updated'])
        update_results['failed_updates'] = len(update_results['failed_sources'])
        update_results['success_rate'] = (update_results['successful_updates'] / update_results['total_sources']) * 100
        
        logger.info(f"Regulatory update completed. Success rate: {update_results['success_rate']:.1f}%")
        
        return update_results
    
    def _count_records(self, data: Dict) -> int:
        """Count total records in collected data"""
        
        count = 0
        for key, value in data.items():
            if isinstance(value, list):
                count += len(value)
            elif isinstance(value, dict) and key not in ['source', 'collection_date', 'base_url']:
                count += len(value)
        
        return count
    
    async def check_for_updates(self) -> Dict:
        """Check if updates are needed based on last update time"""
        
        update_needed = {}
        current_time = datetime.now()
        
        for source_name in self.scrapers.keys():
            last_update = self.last_update.get(source_name)
            
            if last_update is None:
                update_needed[source_name] = {
                    'needs_update': True,
                    'reason': 'Never updated',
                    'priority': 'high'
                }
            else:
                time_since_update = current_time - last_update
                
                # Different update frequencies for different sources
                if source_name == 'frc':
                    max_age = timedelta(days=7)  # Weekly updates for regulations
                elif source_name == 'ngx':
                    max_age = timedelta(days=1)  # Daily updates for market data
                else:
                    max_age = timedelta(days=3)  # Default 3 days
                
                if time_since_update > max_age:
                    update_needed[source_name] = {
                        'needs_update': True,
                        'reason': f'Last updated {time_since_update.days} days ago',
                        'priority': 'medium' if time_since_update.days < 14 else 'high'
                    }
                else:
                    update_needed[source_name] = {
                        'needs_update': False,
                        'reason': f'Updated {time_since_update.days} days ago',
                        'priority': 'low'
                    }
        
        return {
            'check_timestamp': current_time.isoformat(),
            'sources': update_needed,
            'sources_needing_update': [k for k, v in update_needed.items() if v['needs_update']],
            'high_priority_updates': [k for k, v in update_needed.items() if v['priority'] == 'high']
        }
    
    async def update_specific_source(self, source_name: str) -> Dict:
        """Update data from a specific source"""
        
        if source_name not in self.scrapers:
            return {
                'error': f'Unknown source: {source_name}',
                'available_sources': list(self.scrapers.keys())
            }
        
        try:
            logger.info(f"Updating {source_name} data...")
            
            scraper = self.scrapers[source_name]
            data = await scraper.collect_data()
            
            if 'error' not in data:
                self.last_update[source_name] = datetime.now()
                return {
                    'source': source_name,
                    'status': 'success',
                    'records_collected': self._count_records(data),
                    'updated_at': datetime.now().isoformat()
                }
            else:
                return {
                    'source': source_name,
                    'status': 'failed',
                    'error': data['error'],
                    'attempted_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to update {source_name}: {e}")
            return {
                'source': source_name,
                'status': 'failed',
                'error': str(e),
                'attempted_at': datetime.now().isoformat()
            }
    
    def get_update_status(self) -> Dict:
        """Get current update status for all sources"""
        
        status = {
            'current_time': datetime.now().isoformat(),
            'sources': {}
        }
        
        for source_name in self.scrapers.keys():
            last_update = self.last_update.get(source_name)
            
            if last_update:
                time_since_update = datetime.now() - last_update
                status['sources'][source_name] = {
                    'last_updated': last_update.isoformat(),
                    'days_since_update': time_since_update.days,
                    'hours_since_update': round(time_since_update.total_seconds() / 3600, 1),
                    'status': 'current' if time_since_update.days < 3 else 'stale'
                }
            else:
                status['sources'][source_name] = {
                    'last_updated': None,
                    'days_since_update': None,
                    'hours_since_update': None,
                    'status': 'never_updated'
                }
        
        return status