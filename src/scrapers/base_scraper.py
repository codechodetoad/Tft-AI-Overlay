import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

class BaseScraper:
    """Base class for web scrapers with common functionality"""

    def __init__(self, base_url, cache_duration_hours=6):
        self.base_url = base_url
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.last_fetch = {}

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_page(self, url, max_retries=3):
        """Fetch a web page with retry logic"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()

                # Be respectful - rate limit
                time.sleep(1)

                return BeautifulSoup(response.text, 'html.parser')

            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

    def should_fetch(self, key):
        """Check if we should fetch based on cache"""
        if key not in self.last_fetch:
            return True

        return datetime.now() - self.last_fetch[key] > self.cache_duration

    def mark_fetched(self, key):
        """Mark a resource as fetched"""
        self.last_fetch[key] = datetime.now()

    def extract_text_safe(self, element, selector, default=""):
        """Safely extract text from BeautifulSoup element"""
        try:
            found = element.find(selector) if isinstance(selector, str) else element.find(*selector)
            return found.text.strip() if found else default
        except:
            return default

    def extract_float_safe(self, element, selector, default=0.0):
        """Safely extract float from element"""
        text = self.extract_text_safe(element, selector, str(default))
        try:
            # Remove % signs and other characters
            cleaned = ''.join(c for c in text if c.isdigit() or c == '.')
            return float(cleaned) if cleaned else default
        except:
            return default
