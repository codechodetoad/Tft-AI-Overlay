import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta

class TFTDataScraper:
    """
    Web scraper for TFT data

    Sources:
    1. Community Dragon API (free, no key needed) - Champion/item data
    2. MetaTFT (web scraping) - Meta compositions
    """

    def __init__(self, cache_dir="data_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        # Community Dragon API endpoint (Riot's public CDN)
        self.cdragon_base = "https://raw.communitydragon.org/latest/cdragon/tft"

        # Cache expiry (update weekly)
        self.cache_expiry = timedelta(days=7)

    def get_champions_data(self):
        """
        Get champion data from Community Dragon

        Returns:
            dict: Champion stats, traits, costs
        """
        cache_file = os.path.join(self.cache_dir, "champions.json")

        # Check cache
        if self._is_cache_valid(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)

        print("Fetching champion data from Community Dragon...")

        try:
            # Get current set data
            url = f"{self.cdragon_base}/en_us.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract champion info
            champions = {}
            if 'sets' in data:
                latest_set = data['sets'][-1]  # Get latest set

                for champ_key, champ_data in latest_set.get('champions', {}).items():
                    champions[champ_data['name']] = {
                        'cost': champ_data.get('cost', 1),
                        'traits': champ_data.get('traits', []),
                        'stats': {
                            'hp': champ_data.get('stats', {}).get('hp', 0),
                            'mana': champ_data.get('stats', {}).get('mana', 0),
                            'armor': champ_data.get('stats', {}).get('armor', 0),
                            'mr': champ_data.get('stats', {}).get('magicResist', 0),
                            'damage': champ_data.get('stats', {}).get('damage', 0)
                        }
                    }

            # Cache the data
            with open(cache_file, 'w') as f:
                json.dump(champions, f, indent=2)

            return champions

        except Exception as e:
            print(f"Failed to fetch champion data: {e}")
            return self._get_fallback_champions()

    def get_items_data(self):
        """
        Get item data

        Returns:
            dict: Item combinations and effects
        """
        cache_file = os.path.join(self.cache_dir, "items.json")

        if self._is_cache_valid(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)

        print("Fetching item data...")

        try:
            url = f"{self.cdragon_base}/en_us.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            items = {}
            if 'sets' in data:
                latest_set = data['sets'][-1]

                for item_id, item_data in latest_set.get('items', {}).items():
                    items[item_data['name']] = {
                        'effects': item_data.get('effects', {}),
                        'description': item_data.get('desc', ''),
                        'from': item_data.get('from', [])  # Component items
                    }

            with open(cache_file, 'w') as f:
                json.dump(items, f, indent=2)

            return items

        except Exception as e:
            print(f"Failed to fetch item data: {e}")
            return {}

    def get_meta_comps(self):
        """
        Scrape meta compositions from MetaTFT

        Returns:
            list: Top meta compositions with win rates
        """
        cache_file = os.path.join(self.cache_dir, "meta_comps.json")

        if self._is_cache_valid(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)

        print("Scraping meta compositions...")

        try:
            # MetaTFT homepage
            url = "https://www.metatft.com/comps"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            meta_comps = []

            # Find composition cards (structure may vary - this is example)
            comp_cards = soup.find_all('div', class_='comp-card')[:10]  # Top 10

            for card in comp_cards:
                try:
                    comp_name = card.find('h3').text.strip() if card.find('h3') else "Unknown"

                    # Extract traits
                    traits = []
                    trait_elements = card.find_all('span', class_='trait')
                    for trait in trait_elements:
                        traits.append(trait.text.strip())

                    # Extract units
                    units = []
                    unit_elements = card.find_all('div', class_='unit')
                    for unit in unit_elements:
                        units.append(unit.text.strip())

                    meta_comps.append({
                        'name': comp_name,
                        'traits': traits,
                        'units': units,
                        'tier': 'S'  # Assume top comps are S-tier
                    })

                except Exception as e:
                    continue

            # If scraping fails, use fallback
            if not meta_comps:
                meta_comps = self._get_fallback_meta_comps()

            with open(cache_file, 'w') as f:
                json.dump(meta_comps, f, indent=2)

            return meta_comps

        except Exception as e:
            print(f"Failed to scrape meta comps: {e}")
            return self._get_fallback_meta_comps()

    def _is_cache_valid(self, cache_file):
        """Check if cache file exists and is not expired"""
        if not os.path.exists(cache_file):
            return False

        file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        return datetime.now() - file_time < self.cache_expiry

    def _get_fallback_champions(self):
        """Fallback champion data if API fails"""
        return {
            "Ahri": {"cost": 4, "traits": ["Arcanist", "Scholar"], "stats": {"hp": 650, "mana": 60}},
            "Akali": {"cost": 4, "traits": ["Assassin", "Syndicate"], "stats": {"hp": 650, "mana": 50}},
            "Ashe": {"cost": 2, "traits": ["Sniper", "Syndicate"], "stats": {"hp": 550, "mana": 40}},
            "Blitzcrank": {"cost": 2, "traits": ["Bodyguard", "Innovator"], "stats": {"hp": 700, "mana": 60}},
            "Jinx": {"cost": 4, "traits": ["Scrap", "Sister"], "stats": {"hp": 650, "mana": 70}},
            "Vi": {"cost": 3, "traits": ["Enforcer", "Sister"], "stats": {"hp": 750, "mana": 50}},
        }

    def _get_fallback_meta_comps(self):
        """Fallback meta comps if scraping fails"""
        return [
            {
                "name": "Arcanist",
                "traits": ["Arcanist", "Scholar", "Enchanter"],
                "units": ["Ahri", "Viktor", "Lux", "Vex", "Janna"],
                "tier": "S"
            },
            {
                "name": "Assassins",
                "traits": ["Assassin", "Syndicate", "Challenger"],
                "units": ["Akali", "Ekko", "Katarina", "Talon"],
                "tier": "A"
            }
        ]

    def update_all_data(self):
        """Update all cached data"""
        print("Updating all TFT data...")
        self.get_champions_data()
        self.get_items_data()
        self.get_meta_comps()
        print("Data update complete!")


class DataManager:
    """Manage scraped data and provide easy access"""

    def __init__(self):
        self.scraper = TFTDataScraper()
        self.champions = None
        self.items = None
        self.meta_comps = None

    def load_data(self):
        """Load all data"""
        self.champions = self.scraper.get_champions_data()
        self.items = self.scraper.get_items_data()
        self.meta_comps = self.scraper.get_meta_comps()

    def get_champion_info(self, name):
        """Get info for a specific champion"""
        if self.champions is None:
            self.load_data()
        return self.champions.get(name, {})

    def get_comp_recommendation(self, current_units):
        """Recommend which comp to build based on current units"""
        if self.meta_comps is None:
            self.load_data()

        recommendations = []

        for comp in self.meta_comps:
            # Count how many units from meta comp you have
            matches = len(set(current_units) & set(comp['units']))

            if matches > 0:
                recommendations.append({
                    'comp': comp['name'],
                    'matches': matches,
                    'missing': list(set(comp['units']) - set(current_units)),
                    'tier': comp['tier']
                })

        # Sort by matches
        recommendations.sort(key=lambda x: x['matches'], reverse=True)

        return recommendations
