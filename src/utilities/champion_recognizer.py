import cv2
import numpy as np
from PIL import Image
import os
import pytesseract

class ChampionRecognizer:
    """
    Phase 3: Champion recognition using computer vision

    Methods:
    1. Template matching (compare against champion portraits)
    2. OCR on champion names
    3. Color histogram matching
    """

    def __init__(self, templates_dir="champion_templates"):
        self.templates_dir = templates_dir
        self.templates = {}
        self.load_templates()

    def load_templates(self):
        """Load champion portrait templates"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            print(f"Champion templates directory created: {self.templates_dir}")
            print("Add champion portrait images (.png) to this folder for recognition")
            return

        # Load all templates
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(('.png', '.jpg')):
                champ_name = os.path.splitext(filename)[0]
                template_path = os.path.join(self.templates_dir, filename)

                template = cv2.imread(template_path)
                if template is not None:
                    self.templates[champ_name] = template

        print(f"Loaded {len(self.templates)} champion templates")

    def recognize_champion(self, unit_roi):
        """
        Recognize champion from unit ROI

        Args:
            unit_roi: Image region containing the champion

        Returns:
            str: Champion name or "Unknown"
        """
        if isinstance(unit_roi, Image.Image):
            unit_cv = cv2.cvtColor(np.array(unit_roi), cv2.COLOR_RGB2BGR)
        else:
            unit_cv = unit_roi

        # Method 1: Template matching
        if self.templates:
            template_match = self._template_match(unit_cv)
            if template_match:
                return template_match

        # Method 2: OCR (if champion name is visible)
        ocr_match = self._ocr_match(unit_cv)
        if ocr_match:
            return ocr_match

        # Method 3: Color histogram matching
        color_match = self._color_match(unit_cv)
        if color_match:
            return color_match

        return "Unknown"

    def _template_match(self, img):
        """Match using template matching"""
        best_match = None
        best_score = 0.6  # Minimum confidence threshold

        # Resize image to standard size
        img_resized = cv2.resize(img, (64, 64))

        for champ_name, template in self.templates.items():
            # Resize template to match
            template_resized = cv2.resize(template, (64, 64))

            # Template matching
            result = cv2.matchTemplate(img_resized, template_resized, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            if max_val > best_score:
                best_score = max_val
                best_match = champ_name

        return best_match

    def _ocr_match(self, img):
        """Match using OCR on champion name text"""
        try:
            # Preprocess for OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply threshold
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # OCR
            text = pytesseract.image_to_string(thresh, config='--psm 7').strip()

            # Clean up text
            text = ''.join(c for c in text if c.isalpha())

            if len(text) >= 3:
                # Fuzzy match against known champions
                return self._fuzzy_match_champion(text)

        except Exception as e:
            pass

        return None

    def _color_match(self, img):
        """Match using color histogram (basic)"""
        # Each champion has a dominant color scheme
        # This is a simple fallback method

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Calculate dominant hue
        hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
        dominant_hue = np.argmax(hist)

        # Champion color associations (examples)
        color_champions = {
            range(0, 15): ["Ahri", "Brand"],      # Red/Pink
            range(15, 30): ["Jinx", "Lux"],       # Yellow/Gold
            range(100, 130): ["Ashe", "Ezreal"],  # Blue
            range(40, 80): ["Zed", "Akali"],      # Green/Teal
        }

        for hue_range, champions in color_champions.items():
            if dominant_hue in hue_range:
                return champions[0]  # Return first match

        return None

    def _fuzzy_match_champion(self, text):
        """Fuzzy match text to known champion names"""
        # List of champion names (extend this)
        known_champions = [
            "Ahri", "Akali", "Ashe", "Blitzcrank", "Caitlyn", "Draven",
            "Ekko", "Ezreal", "Fiora", "Garen", "Graves", "Jinx",
            "Katarina", "Lux", "Malzahar", "Nami", "Senna", "Talon",
            "Thresh", "Twisted Fate", "Vayne", "Vi", "Viktor", "Warwick",
            "Yasuo", "Zed", "Ziggs", "Zyra"
        ]

        text_lower = text.lower()

        # Exact match
        for champ in known_champions:
            if text_lower == champ.lower():
                return champ

        # Partial match (at least 4 characters)
        if len(text) >= 4:
            for champ in known_champions:
                if text_lower in champ.lower() or champ.lower() in text_lower:
                    return champ

        return None

    def create_template_from_screenshot(self, screenshot, unit_position, champion_name):
        """
        Save a champion template from a screenshot

        Args:
            screenshot: Full game screenshot
            unit_position: (x, y, w, h) of champion unit
            champion_name: Name to save template as
        """
        if isinstance(screenshot, Image.Image):
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        else:
            img = screenshot

        x, y, w, h = unit_position
        unit_roi = img[y:y+h, x:x+w]

        # Save template
        template_path = os.path.join(self.templates_dir, f"{champion_name}.png")
        cv2.imwrite(template_path, unit_roi)

        # Reload templates
        self.templates[champion_name] = unit_roi

        print(f"Saved template for {champion_name}")

    def batch_recognize(self, unit_rois):
        """
        Recognize multiple champions at once

        Args:
            unit_rois: List of unit ROI images

        Returns:
            List of champion names
        """
        champions = []

        for roi in unit_rois:
            champ = self.recognize_champion(roi)
            champions.append(champ)

        return champions


class ItemRecognizer:
    """Recognize items on champions"""

    def __init__(self):
        # Common item colors for detection
        self.item_signatures = {
            "Blue Buff": ([100, 100, 100], [130, 255, 255]),  # Blue HSV range
            "Infinity Edge": ([0, 0, 200], [180, 30, 255]),   # Silver/white
            "Sunfire Cape": ([0, 100, 100], [20, 255, 255]),  # Orange/red
        }

    def detect_items(self, unit_roi):
        """
        Detect items on a champion

        Returns:
            List of item names (max 3)
        """
        if isinstance(unit_roi, Image.Image):
            img = cv2.cvtColor(np.array(unit_roi), cv2.COLOR_RGB2BGR)
        else:
            img = unit_roi

        # Items appear as small icons on the unit
        # Typically bottom-left of unit portrait

        h, w = img.shape[:2]
        item_region = img[int(h*0.7):, :int(w*0.5)]

        items = []

        # Convert to HSV
        hsv = cv2.cvtColor(item_region, cv2.COLOR_BGR2HSV)

        for item_name, (lower, upper) in self.item_signatures.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

            # Check if item color is present
            if np.count_nonzero(mask) > 50:  # Threshold
                items.append(item_name)

            if len(items) >= 3:
                break

        return items
