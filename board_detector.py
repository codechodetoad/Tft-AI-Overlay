import cv2
import numpy as np
from PIL import Image

class BoardDetector:
    """Phase 3: Computer vision for board detection"""

    def __init__(self):
        self.board_positions = []
        self.bench_positions = []

    def detect_units_on_board(self, img):
        """
        Detect champion positions on the board using computer vision

        Args:
            img: PIL Image or numpy array

        Returns:
            List of detected unit positions
        """
        # Convert PIL to OpenCV format
        if isinstance(img, Image.Image):
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Detect hexagonal board tiles (TFT uses hex grid)
        detected_positions = self._find_hex_tiles(hsv)

        return detected_positions

    def _find_hex_tiles(self, hsv_img):
        """Find hexagonal tiles on the TFT board"""
        positions = []

        # Define color ranges for occupied vs empty tiles
        # These are approximate - adjust based on actual game colors
        occupied_lower = np.array([0, 50, 50])
        occupied_upper = np.array([180, 255, 255])

        # Create mask for potential units
        mask = cv2.inRange(hsv_img, occupied_lower, occupied_upper)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            # Filter by size (adjust threshold based on screen resolution)
            if 100 < area < 5000:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    positions.append((cx, cy))

        return positions

    def detect_stars(self, img, unit_region):
        """
        Detect star level of a unit (1, 2, or 3 stars)

        Args:
            img: Full screenshot
            unit_region: (x, y, w, h) region containing the unit

        Returns:
            Number of stars (1-3)
        """
        x, y, w, h = unit_region

        # Convert to numpy if needed
        if isinstance(img, Image.Image):
            img_np = np.array(img)
        else:
            img_np = img

        # Extract unit region
        unit_img = img_np[y:y+h, x:x+w]

        # Convert to HSV
        hsv = cv2.cvtColor(unit_img, cv2.COLOR_RGB2HSV)

        # Stars are typically gold/yellow colored
        star_lower = np.array([15, 100, 100])
        star_upper = np.array([35, 255, 255])

        # Create mask for stars
        star_mask = cv2.inRange(hsv, star_lower, star_upper)

        # Count star shapes/regions
        contours, _ = cv2.findContours(star_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Count significant contours as stars
        star_count = len([c for c in contours if cv2.contourArea(c) > 10])

        return min(star_count, 3)  # Cap at 3 stars

    def detect_items(self, img, unit_region):
        """
        Detect items on a unit

        Args:
            img: Full screenshot
            unit_region: (x, y, w, h) region containing the unit

        Returns:
            Number of items (0-3)
        """
        x, y, w, h = unit_region

        if isinstance(img, Image.Image):
            img_np = np.array(img)
        else:
            img_np = img

        unit_img = img_np[y:y+h, x:x+w]

        # Items typically appear as colored icons below/on the unit
        # This is a simplified detection - real implementation would need training data

        gray = cv2.cvtColor(unit_img, cv2.COLOR_RGB2GRAY)

        # Detect bright spots (item icons)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Count item-sized contours
        item_count = len([c for c in contours if 50 < cv2.contourArea(c) < 500])

        return min(item_count, 3)  # Max 3 items per unit

    def map_screen_to_hex_grid(self, screen_positions):
        """
        Convert screen pixel positions to hex grid coordinates

        TFT board is 7 columns x 4 rows in hexagonal pattern

        Args:
            screen_positions: List of (x, y) pixel coordinates

        Returns:
            List of (col, row) hex grid positions
        """
        hex_positions = []

        # This requires calibration based on screen resolution
        # Approximate mapping for 1920x1080
        for x, y in screen_positions:
            # Convert pixels to hex grid (simplified)
            col = int((x - 500) / 120)  # Adjust offsets based on actual layout
            row = int((y - 400) / 100)

            # Validate bounds
            if 0 <= col < 7 and 0 <= row < 4:
                hex_positions.append((col, row))

        return hex_positions

    def get_board_region_coords(self, resolution=(1920, 1080)):
        """
        Get typical coordinates for board regions based on resolution

        Args:
            resolution: (width, height) screen resolution

        Returns:
            Dictionary with board, bench, and shop regions
        """
        width, height = resolution

        # These are approximate ratios - adjust based on actual game layout
        return {
            "board": {
                "left": int(width * 0.25),
                "top": int(height * 0.35),
                "width": int(width * 0.5),
                "height": int(height * 0.4)
            },
            "bench": {
                "left": int(width * 0.2),
                "top": int(height * 0.8),
                "width": int(width * 0.6),
                "height": int(height * 0.15)
            },
            "shop": {
                "left": int(width * 0.3),
                "top": int(height * 0.7),
                "width": int(width * 0.4),
                "height": int(height * 0.08)
            },
            "stats": {
                "left": 0,
                "top": 0,
                "width": int(width * 0.2),
                "height": int(height * 0.1)
            }
        }
