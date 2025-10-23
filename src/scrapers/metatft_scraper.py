from .base_scraper import BaseScraper
import re

class MetaTFTScraper(BaseScraper):
    """Scraper for MetaTFT.com data"""

    BASE_URL = "https://www.metatft.com"

    def __init__(self):
        super().__init__(self.BASE_URL)

    def scrape_compositions(self):
        """Scrape top meta compositions"""
        if not self.should_fetch('compositions'):
            return []

        try:
            soup = self.fetch_page(f"{self.BASE_URL}/comps")
            compositions = []

            # Find composition cards
            comp_cards = soup.find_all('div', class_='comp-card')[:15]

            for card in comp_cards:
                try:
                    comp_data = {
                        'name': self.extract_text_safe(card, 'h3', 'Unknown Comp'),
                        'tier': self._extract_tier(card),
                        'win_rate': self.extract_float_safe(card, '.win-rate', 0.0),
                        'avg_placement': self.extract_float_safe(card, '.avg-place', 4.5),
                        'champions': self._extract_champions(card),
                        'traits': self._extract_traits(card)
                    }

                    compositions.append(comp_data)

                except Exception as e:
                    continue

            self.mark_fetched('compositions')
            return compositions

        except Exception as e:
            print(f"Failed to scrape compositions: {e}")
            return self._get_fallback_compositions()

    def scrape_augments(self):
        """Scrape augment tier list"""
        if not self.should_fetch('augments'):
            return []

        try:
            soup = self.fetch_page(f"{self.BASE_URL}/augments")
            augments = []

            # Find augment sections by tier
            for tier_rank in ['S', 'A', 'B', 'C', 'D']:
                tier_section = soup.find('div', {'data-tier': tier_rank})

                if tier_section:
                    aug_items = tier_section.find_all('div', class_='augment-item')

                    for aug in aug_items:
                        try:
                            augments.append({
                                'name': self.extract_text_safe(aug, '.augment-name'),
                                'tier_list_rank': tier_rank,
                                'tier': self._map_augment_tier(aug),
                                'win_rate': self.extract_float_safe(aug, '.win-rate', 50.0),
                                'pick_rate': self.extract_float_safe(aug, '.pick-rate', 10.0)
                            })
                        except:
                            continue

            self.mark_fetched('augments')
            return augments

        except Exception as e:
            print(f"Failed to scrape augments: {e}")
            return self._get_fallback_augments()

    def scrape_items(self):
        """Scrape item priority data"""
        if not self.should_fetch('items'):
            return []

        try:
            soup = self.fetch_page(f"{self.BASE_URL}/items")
            items = []

            item_rows = soup.find_all('tr', class_='item-row')

            for row in item_rows:
                try:
                    items.append({
                        'name': self.extract_text_safe(row, '.item-name'),
                        'priority_score': self.extract_float_safe(row, '.priority-score', 5.0),
                        'components': self._extract_components(row),
                        'recommended_for': self._extract_recommended_champs(row)
                    })
                except:
                    continue

            self.mark_fetched('items')
            return items

        except Exception as e:
            print(f"Failed to scrape items: {e}")
            return self._get_fallback_items()

    def _extract_tier(self, card):
        """Extract tier rank (S/A/B/C/D)"""
        tier_badge = card.find('span', class_='tier-badge')
        if tier_badge:
            text = tier_badge.text.strip().upper()
            if text in ['S', 'A', 'B', 'C', 'D']:
                return text
        return 'B'

    def _extract_champions(self, card):
        """Extract champion list from composition card"""
        champ_elements = card.find_all('span', class_='champion-name')
        return [elem.text.strip() for elem in champ_elements]

    def _extract_traits(self, card):
        """Extract active traits"""
        trait_elements = card.find_all('span', class_='trait')
        return [elem.text.strip() for elem in trait_elements]

    def _extract_components(self, row):
        """Extract item components"""
        component_spans = row.find_all('span', class_='component')
        return [span.text.strip() for span in component_spans]

    def _extract_recommended_champs(self, row):
        """Extract champions this item is good on"""
        champ_div = row.find('div', class_='recommended-champs')
        if champ_div:
            return [span.text.strip() for span in champ_div.find_all('span')]
        return []

    def _map_augment_tier(self, aug_element):
        """Map augment HTML element to tier (Silver/Gold/Prismatic)"""
        classes = aug_element.get('class', [])
        if 'prismatic' in classes:
            return 'Prismatic'
        elif 'gold' in classes:
            return 'Gold'
        else:
            return 'Silver'

    def _get_fallback_compositions(self):
        """Fallback data if scraping fails"""
        return [
            {
                'name': 'Reroll Comp',
                'tier': 'A',
                'win_rate': 55.0,
                'avg_placement': 3.8,
                'champions': ['Low cost units'],
                'traits': ['Reroll trait']
            },
            {
                'name': 'Fast 8 Comp',
                'tier': 'S',
                'win_rate': 60.0,
                'avg_placement': 3.2,
                'champions': ['High cost units'],
                'traits': ['Legendary trait']
            }
        ]

    def _get_fallback_augments(self):
        """Fallback augment data"""
        return [
            {'name': 'Combat Training', 'tier_list_rank': 'S', 'tier': 'Silver', 'win_rate': 55.0},
            {'name': 'Featherweights', 'tier_list_rank': 'A', 'tier': 'Gold', 'win_rate': 52.0}
        ]

    def _get_fallback_items(self):
        """Fallback item data"""
        return [
            {'name': 'Infinity Edge', 'priority_score': 9.0, 'components': ['BF Sword', 'BF Sword']},
            {'name': 'Blue Buff', 'priority_score': 8.5, 'components': ['Tear', 'Tear']}
        ]
