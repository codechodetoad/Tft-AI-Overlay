from .metatft_scraper import MetaTFTScraper
from datetime import datetime, timedelta
import json
import os

class ScrapingOrchestrator:
    """Orchestrates all web scraping activities"""

    def __init__(self, db_manager):
        self.db = db_manager
        self.metatft = MetaTFTScraper()
        self.cache_file = 'data/scraper_cache.json'
        self.last_update_file = 'data/last_update.json'

    def update_all_data(self, force=False):
        """Update all scraped data"""
        if not force and not self._should_update():
            print("Data is up to date. Use force=True to update anyway.")
            return

        print("Starting data update...")

        # Update compositions
        print("Scraping compositions...")
        comps = self.metatft.scrape_compositions()
        for comp in comps:
            try:
                comp['patch'] = 'current'
                self.db.upsert_composition(comp)
            except Exception as e:
                print(f"Failed to save comp {comp.get('name')}: {e}")

        # Update augments
        print("Scraping augments...")
        augments = self.metatft.scrape_augments()
        for aug in augments:
            try:
                self.db.upsert_augment(aug)
            except Exception as e:
                print(f"Failed to save augment {aug.get('name')}: {e}")

        # Update items
        print("Scraping items...")
        items = self.metatft.scrape_items()
        for item in items:
            try:
                self.db.upsert_item(item)
            except Exception as e:
                print(f"Failed to save item {item.get('name')}: {e}")

        # Mark update time
        self._mark_updated()

        print(f"Data update complete! Updated {len(comps)} comps, {len(augments)} augments, {len(items)} items.")

    def _should_update(self):
        """Check if we should update based on last update time"""
        if not os.path.exists(self.last_update_file):
            return True

        try:
            with open(self.last_update_file, 'r') as f:
                data = json.load(f)
                last_update = datetime.fromisoformat(data['last_update'])

                # Update every 6 hours
                return datetime.now() - last_update > timedelta(hours=6)
        except:
            return True

    def _mark_updated(self):
        """Mark that we just updated"""
        os.makedirs(os.path.dirname(self.last_update_file), exist_ok=True)

        with open(self.last_update_file, 'w') as f:
            json.dump({
                'last_update': datetime.now().isoformat()
            }, f)

    def get_last_update_time(self):
        """Get last update timestamp"""
        if not os.path.exists(self.last_update_file):
            return None

        try:
            with open(self.last_update_file, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_update'])
        except:
            return None
