import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter
from dotenv import load_dotenv
import os

load_dotenv()

class OCRReader:
    def __init__(self):
        # Set Tesseract path if specified in environment
        tesseract_path = os.getenv('TESSERACT_PATH')
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def preprocess_image(self, img):
        """
        Preprocess image for better OCR results

        Args:
            img: PIL Image object

        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale
        img = img.convert('L')

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        # Sharpen
        img = img.filter(ImageFilter.SHARPEN)

        return img

    def read_text(self, img, preprocess=True):
        """
        Extract text from image

        Args:
            img: PIL Image object
            preprocess: Whether to preprocess the image

        Returns:
            Extracted text as string
        """
        if preprocess:
            img = self.preprocess_image(img)

        try:
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def read_game_stats(self, img):
        """
        Extract game statistics from screenshot
        This is a TFT-specific method

        Args:
            img: PIL Image object of game screen

        Returns:
            Dictionary with extracted game stats
        """
        text = self.read_text(img)

        game_stats = {
            "level": self._extract_level(text),
            "gold": self._extract_gold(text),
            "health": self._extract_health(text),
            "stage": self._extract_stage(text)
        }

        return game_stats

    def _extract_level(self, text):
        """Extract player level from text"""
        # Look for patterns like "Level 5" or "Lvl 5" or just number near "level"
        patterns = [
            r'(?:Level|Lvl)[\s:]*(\d+)',
            r'Level\s*(\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0

    def _extract_gold(self, text):
        """Extract gold amount from text"""
        # Look for patterns like "45 gold" or number followed by 'g'
        patterns = [
            r'(\d+)\s*(?:gold|Gold|GOLD)',
            r'Gold[\s:]*(\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 0

    def _extract_health(self, text):
        """Extract health/HP from text"""
        patterns = [
            r'(\d+)\s*(?:HP|hp|health|Health)',
            r'(?:HP|health)[\s:]*(\d+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 100

    def _extract_stage(self, text):
        """Extract game stage from text"""
        # Look for patterns like "3-2" or "Stage 3-2"
        pattern = r'(\d+-\d+)'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return ""

    def read_unit_names(self, img):
        """
        Extract unit names from a region of the screen

        Args:
            img: PIL Image object containing units

        Returns:
            List of detected unit names
        """
        text = self.read_text(img)

        # Common TFT unit names (you can expand this list)
        known_units = [
            "Ahri", "Akali", "Ashe", "Azir", "Blitzcrank",
            "Caitlyn", "Cassiopeia", "Chogath", "Draven", "Ekko",
            "Ezreal", "Fiora", "Garen", "Graves", "Hecarim",
            "Heimerdinger", "Janna", "Jarvan", "Jax", "Jayce",
            "Jinx", "Kaisa", "Kalista", "Karma", "Kassadin",
            "Katarina", "Kayle", "Kennen", "Kindred", "Leona",
            "Lulu", "Lux", "Malphite", "Maokai", "Morgana",
            "Nami", "Neeko", "Nidalee", "Nocturne", "Nunu",
            "Pantheon", "Poppy", "Pyke", "Rakan", "Renekton",
            "Riven", "Sejuani", "Senna", "Sett", "Shen",
            "Shyvana", "Sivir", "Sona", "Soraka", "Swain",
            "Syndra", "Tahm Kench", "Talon", "Teemo", "Thresh",
            "Tristana", "Twisted Fate", "Urgot", "Varus", "Vayne",
            "Veigar", "Vi", "Viktor", "Vladimir", "Volibear",
            "Warwick", "Wukong", "Xayah", "Xerath", "Yasuo",
            "Zed", "Ziggs", "Zilean", "Zoe", "Zyra"
        ]

        detected_units = []
        for unit in known_units:
            if unit.lower() in text.lower():
                detected_units.append(unit)

        return detected_units

    def detect_shop_units(self, img, shop_region=None):
        """
        Detect units available in the shop

        Args:
            img: PIL Image object
            shop_region: Tuple (left, top, width, height) of shop area

        Returns:
            List of unit names in shop
        """
        if shop_region:
            img = img.crop((
                shop_region[0],
                shop_region[1],
                shop_region[0] + shop_region[2],
                shop_region[1] + shop_region[3]
            ))

        return self.read_unit_names(img)
