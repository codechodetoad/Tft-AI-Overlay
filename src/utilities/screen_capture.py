import mss
import mss.tools
from PIL import Image
import os
import sys
import subprocess
from datetime import datetime

class ScreenCapture:
    def __init__(self):
        self.is_wsl = 'microsoft' in os.uname().release.lower()

        if not self.is_wsl:
            self.sct = mss.mss()

        self.capture_dir = "captures"

        # Create captures directory if it doesn't exist
        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir)

    def capture_full_screen(self):
        """Capture the entire screen"""
        if self.is_wsl:
            return self._capture_wsl()

        monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)

        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img

    def _capture_wsl(self):
        """Capture screen from WSL using PowerShell"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Use absolute path in the project captures directory
        wsl_path = os.path.abspath(os.path.join(self.capture_dir, f"temp_{timestamp}.png"))

        # Convert WSL path to Windows path
        # Get the current working directory's Windows path
        wsl_cwd = os.getcwd()
        if wsl_cwd.startswith('/mnt/'):
            # Convert /mnt/c/path/to/file to C:\path\to\file
            drive = wsl_cwd[5].upper()
            windows_path = f"{drive}:{wsl_cwd[6:]}".replace("/", "\\")
            windows_temp = os.path.join(windows_path, self.capture_dir, f"temp_{timestamp}.png").replace("/", "\\")
        else:
            raise Exception("Not running in WSL /mnt/ path")

        # PowerShell script to capture screen
        ps_script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save('{windows_temp}')
$graphics.Dispose()
$bitmap.Dispose()
"""

        try:
            subprocess.run(['powershell.exe', '-Command', ps_script], check=True, capture_output=True)
            img = Image.open(wsl_path)
            os.remove(wsl_path)  # Clean up temp file
            return img
        except Exception as e:
            raise Exception(f"WSL screen capture failed: {e}")

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
