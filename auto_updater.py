import threading
import time
from screen_capture import ScreenCapture
from ocr_reader import OCRReader
from board_detector import BoardDetector

class AutoUpdater:
    """Phase 4: Real-time automatic game state updates"""

    def __init__(self, game_state, update_callback=None):
        self.game_state = game_state
        self.update_callback = update_callback
        self.running = False
        self.thread = None

        # Initialize components
        self.screen_capture = ScreenCapture()
        self.ocr_reader = OCRReader()
        self.board_detector = BoardDetector()

        # Update interval in seconds
        self.update_interval = 3.0

    def start(self):
        """Start automatic updates"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop automatic updates"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)

    def _update_loop(self):
        """Main update loop running in background thread"""
        while self.running:
            try:
                self._perform_update()
            except Exception as e:
                print(f"Auto-update error: {e}")

            time.sleep(self.update_interval)

    def _perform_update(self):
        """Perform a single update cycle"""
        # Capture screen
        img = self.screen_capture.capture_full_screen()

        # Extract stats via OCR
        stats = self.ocr_reader.read_game_stats(img)

        # Update game state if valid data detected
        if stats['level'] > 0:
            self.game_state.level = stats['level']
            self.game_state.gold = stats['gold']
            self.game_state.health = stats['health']
            self.game_state.stage = stats['stage']

            # Try to detect board composition
            regions = self.board_detector.get_board_region_coords()

            # Detect units in shop
            shop_region = regions['shop']
            shop_img = img.crop((
                shop_region['left'],
                shop_region['top'],
                shop_region['left'] + shop_region['width'],
                shop_region['top'] + shop_region['height']
            ))

            shop_units = self.ocr_reader.detect_shop_units(shop_img)
            if shop_units:
                self.game_state.available_shops = shop_units

            # Notify callback if provided
            if self.update_callback:
                self.update_callback()

    def set_update_interval(self, seconds):
        """Change the update interval"""
        self.update_interval = max(1.0, seconds)  # Minimum 1 second

    def is_running(self):
        """Check if auto-updater is running"""
        return self.running
