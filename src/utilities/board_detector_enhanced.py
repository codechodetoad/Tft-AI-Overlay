import cv2
import numpy as np
from PIL import Image
import pytesseract

class BoardDetectorEnhanced:
    """Enhanced Phase 3: Advanced computer vision for TFT board detection"""

    def __init__(self):
        self.board_region = None
        self.bench_region = None
        self.shop_region = None

        # Calibration data (adjust per resolution)
        self.calibration = {
            "1920x1080": {
                "board": (480, 200, 960, 600),
                "bench": (384, 880, 1152, 120),
                "shop": (576, 720, 768, 100),
                "stats": (10, 10, 250, 100)
            },
            "2560x1440": {
                "board": (640, 267, 1280, 800),
                "bench": (512, 1173, 1536, 160),
                "shop": (768, 960, 1024, 133),
                "stats": (13, 13, 333, 133)
            }
        }

    def detect_board_state(self, img):
        """
        Comprehensive board state detection

        Returns:
            dict with units, bench, shop, stats
        """
        if isinstance(img, Image.Image):
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        else:
            img_cv = img

        height, width = img_cv.shape[:2]
        resolution = f"{width}x{height}"

        # Get calibrated regions or use defaults
        regions = self.calibration.get(resolution, self.calibration["1920x1080"])

        result = {
            "board_units": self.detect_board_units(img_cv, regions["board"]),
            "bench_units": self.detect_bench_units(img_cv, regions["bench"]),
            "shop_units": self.detect_shop_units(img_cv, regions["shop"]),
            "unit_count": 0
        }

        result["unit_count"] = len(result["board_units"])

        return result

    def detect_board_units(self, img, region):
        """
        Detect units on the battle board

        Args:
            img: OpenCV image
            region: (x, y, w, h) tuple

        Returns:
            List of detected units with positions and stars
        """
        x, y, w, h = region
        board_roi = img[y:y+h, x:x+w]

        # Convert to HSV for better detection
        hsv = cv2.cvtColor(board_roi, cv2.COLOR_BGR2HSV)

        units = []

        # Detect champion portraits (they have specific color characteristics)
        # Method 1: Edge detection for unit borders
        gray = cv2.cvtColor(board_roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Find contours (potential unit locations)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)

            # Filter by size (units are roughly 60x60 to 100x100 pixels at 1080p)
            if 2000 < area < 15000:
                rect = cv2.boundingRect(contour)
                cx, cy, cw, ch = rect

                # Extract unit ROI
                unit_roi = board_roi[cy:cy+ch, cx:cx+cw]

                # Detect stars for this unit
                stars = self._detect_stars_in_roi(unit_roi)

                units.append({
                    "position": (cx + x, cy + y),
                    "size": (cw, ch),
                    "stars": stars,
                    "hex_pos": self._pixel_to_hex(cx, cy, w, h)
                })

        return units

    def detect_bench_units(self, img, region):
        """Detect units on the bench"""
        x, y, w, h = region
        bench_roi = img[y:y+h, x:x+w]

        # Bench units are in a horizontal row
        # Divide bench into 9 slots
        slot_width = w // 9
        units = []

        for i in range(9):
            slot_x = i * slot_width
            slot_roi = bench_roi[:, slot_x:slot_x+slot_width]

            # Check if slot is occupied (not mostly dark/empty)
            if self._is_slot_occupied(slot_roi):
                stars = self._detect_stars_in_roi(slot_roi)
                units.append({
                    "slot": i,
                    "stars": stars
                })

        return units

    def detect_shop_units(self, img, region):
        """Detect units in the shop"""
        x, y, w, h = region
        shop_roi = img[y:y+h, x:x+w]

        # Shop has 5 slots
        slot_width = w // 5
        units = []

        for i in range(5):
            slot_x = i * slot_width
            slot_roi = shop_roi[:, slot_x:slot_x+slot_width]

            # Try OCR on champion name
            try:
                # Preprocess for OCR
                gray = cv2.cvtColor(slot_roi, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                text = pytesseract.image_to_string(thresh, config='--psm 7').strip()

                if text and len(text) > 2:
                    units.append({
                        "slot": i,
                        "name": text
                    })
            except:
                pass

        return units

    def _detect_stars_in_roi(self, roi):
        """
        Detect number of stars (1-3) in a unit ROI

        Stars are bright yellow/gold at bottom of unit portrait
        """
        if roi.size == 0:
            return 1

        # Focus on bottom 20% of ROI where stars appear
        h = roi.shape[0]
        star_region = roi[int(h * 0.8):, :]

        # Convert to HSV
        hsv = cv2.cvtColor(star_region, cv2.COLOR_BGR2HSV)

        # Gold/yellow color range for stars
        lower_gold = np.array([15, 100, 150])
        upper_gold = np.array([35, 255, 255])

        mask = cv2.inRange(hsv, lower_gold, upper_gold)

        # Count bright spots (stars)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter small noise
        star_contours = [c for c in contours if cv2.contourArea(c) > 10]

        stars = min(len(star_contours), 3)

        return stars if stars > 0 else 1

    def _is_slot_occupied(self, slot_roi):
        """Check if a bench/shop slot has a unit"""
        if slot_roi.size == 0:
            return False

        # Calculate average brightness
        gray = cv2.cvtColor(slot_roi, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)

        # Empty slots are darker
        return avg_brightness > 40

    def _pixel_to_hex(self, px, py, board_w, board_h):
        """
        Convert pixel coordinates to hex grid position

        TFT board is 7 columns x 4 rows
        """
        # Simple grid mapping
        col = int((px / board_w) * 7)
        row = int((py / board_h) * 4)

        col = max(0, min(col, 6))
        row = max(0, min(row, 3))

        return (col, row)

    def visualize_detections(self, img, detections):
        """
        Draw detected units on image for debugging

        Args:
            img: PIL Image
            detections: Output from detect_board_state()

        Returns:
            PIL Image with annotations
        """
        if isinstance(img, Image.Image):
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        else:
            img_cv = img.copy()

        # Draw board units
        for unit in detections.get("board_units", []):
            pos = unit["position"]
            size = unit["size"]
            stars = unit["stars"]

            # Draw rectangle
            cv2.rectangle(img_cv, pos, (pos[0] + size[0], pos[1] + size[1]), (0, 255, 0), 2)

            # Draw stars
            cv2.putText(img_cv, f"{stars}★", (pos[0], pos[1] - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 215, 0), 2)

        # Draw bench units
        for unit in detections.get("bench_units", []):
            slot = unit["slot"]
            # Visual indicator on bench

        # Convert back to PIL
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)

    def calibrate_for_resolution(self, img):
        """Auto-detect regions for current resolution"""
        if isinstance(img, Image.Image):
            width, height = img.size
        else:
            height, width = img.shape[:2]

        # Calculate relative positions based on resolution
        regions = {
            "board": (
                int(width * 0.25),
                int(height * 0.15),
                int(width * 0.5),
                int(height * 0.55)
            ),
            "bench": (
                int(width * 0.2),
                int(height * 0.82),
                int(width * 0.6),
                int(height * 0.11)
            ),
            "shop": (
                int(width * 0.3),
                int(height * 0.67),
                int(width * 0.4),
                int(height * 0.09)
            ),
            "stats": (
                10, 10,
                int(width * 0.13),
                int(height * 0.09)
            )
        }

        return regions
