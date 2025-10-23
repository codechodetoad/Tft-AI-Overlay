#!/usr/bin/env python3
"""
TFT AI Overlay - Main Launcher
Automatically runs the enhanced Phase 5 overlay
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main.overlay_enhanced import TFTOverlayEnhanced
import tkinter as tk

if __name__ == "__main__":
    print("Starting TFT Overlay (Phase 5)...")
    root = tk.Tk()
    app = TFTOverlayEnhanced(root)
    root.mainloop()
