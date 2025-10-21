import mss
import mss.tools
from PIL import Image
import os
from datetime import datetime

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
        self.capture_dir = "captures"

        # Create captures directory if it doesn't exist
        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir)

    def capture_full_screen(self):
        """Capture the entire screen"""
        monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)

        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

    def capture_region(self, left, top, width, height):
        """
        Capture a specific region of the screen

        Args:
            left: X coordinate of top-left corner
            top: Y coordinate of top-left corner
            width: Width of the region
            height: Height of the region

        Returns:
            PIL Image object
        """
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }

        screenshot = self.sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

    def capture_game_region(self):
        """
        Capture the game region (TFT-specific)
        This is a placeholder - you'll need to adjust coordinates based on your screen

        For 1920x1080 resolution:
        - Game typically runs in center
        - UI elements are at specific locations
        """
        # These coordinates are examples - adjust based on your resolution
        # Full HD (1920x1080) example
        return self.capture_region(0, 0, 1920, 1080)

    def save_capture(self, img, filename=None):
        """
        Save captured image to disk

        Args:
            img: PIL Image object
            filename: Optional custom filename

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capture_{timestamp}.png"

        filepath = os.path.join(self.capture_dir, filename)
        img.save(filepath)
        return filepath

    def get_monitor_info(self):
        """Get information about all monitors"""
        return self.sct.monitors

    def capture_and_save(self, region=None):
        """
        Convenience method to capture and save in one step

        Args:
            region: Tuple of (left, top, width, height) or None for full screen

        Returns:
            Path to saved file
        """
        if region:
            img = self.capture_region(*region)
        else:
            img = self.capture_full_screen()

        return self.save_capture(img)
