# Makefile for TFT AI Overlay

# Variables
PYTHON = venv/bin/python
PIP = venv/bin/pip
VENV = venv

# Default target
.PHONY: help
help:
	@echo "TFT AI Overlay - Available Commands:"
	@echo ""
	@echo "  make run          - Run the basic overlay"
	@echo "  make run-enhanced - Run Phase 5 enhanced overlay"
	@echo "  make setup        - Initial setup (create venv + install deps)"
	@echo "  make install      - Install/update dependencies"
	@echo "  make venv         - Create virtual environment"
	@echo "  make clean        - Remove virtual environment and cache files"
	@echo "  make test         - Test the installation"
	@echo "  make ocr-test     - Test Tesseract OCR installation"
	@echo "  make capture-test - Test screen capture"
	@echo ""

# Run the basic application
.PHONY: run
run:
	@echo "Starting TFT Overlay (Basic)..."
	$(PYTHON) overlay.py

# Run the Phase 5 enhanced application
.PHONY: run-enhanced
run-enhanced:
	@echo "Starting TFT Overlay (Phase 5 Enhanced)..."
	$(PYTHON) overlay_enhanced.py

# Initial setup
.PHONY: setup
setup: venv install
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Install Tesseract OCR (see QUICKSTART.md)"
	@echo "2. Run: make run-enhanced"
	@echo ""

# Create virtual environment
.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "✅ Virtual environment created"

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

# Update dependencies
.PHONY: update
update:
	@echo "Updating dependencies..."
	$(PIP) install --upgrade -r requirements.txt
	@echo "✅ Dependencies updated"

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✅ Cleanup complete"

# Test installation
.PHONY: test
test:
	@echo "Testing Python installation..."
	@$(PYTHON) --version
	@echo ""
	@echo "Testing imports..."
	@$(PYTHON) -c "import tkinter; print('✅ tkinter OK')" || echo "❌ tkinter FAILED"
	@$(PYTHON) -c "import PIL; print('✅ Pillow OK')" || echo "❌ Pillow FAILED"
	@$(PYTHON) -c "import mss; print('✅ mss OK')" || echo "❌ mss FAILED"
	@$(PYTHON) -c "import pytesseract; print('✅ pytesseract OK')" || echo "❌ pytesseract FAILED"
	@$(PYTHON) -c "import cv2; print('✅ opencv OK')" || echo "❌ opencv FAILED"
	@$(PYTHON) -c "import numpy; print('✅ numpy OK')" || echo "❌ numpy FAILED"
	@echo ""
	@echo "Testing complete!"

# Test OCR
.PHONY: ocr-test
ocr-test:
	@echo "Testing Tesseract OCR..."
	@tesseract --version || echo "❌ Tesseract not found. Install with: sudo apt-get install tesseract-ocr"

# Test screen capture
.PHONY: capture-test
capture-test:
	@echo "Testing screen capture..."
	@$(PYTHON) -c "from screen_capture import ScreenCapture; sc = ScreenCapture(); print('Monitors:', sc.get_monitor_info()); print('✅ Screen capture OK')"


# Install Tesseract (Ubuntu/Debian)
.PHONY: install-tesseract
install-tesseract:
	@echo "Installing Tesseract OCR..."
	sudo apt-get update
	sudo apt-get install -y tesseract-ocr
	@echo "✅ Tesseract installed"
	@tesseract --version

# Check environment
.PHONY: check-env
check-env:
	@echo "Environment Check:"
	@echo ""
	@echo "Python: $$($(PYTHON) --version 2>&1)"
	@echo "Pip: $$($(PIP) --version 2>&1)"
	@echo ""
	@echo "Virtual environment: $$(test -d $(VENV) && echo '✅ exists' || echo '❌ not found')"
	@echo "Dependencies installed: $$(test -f $(VENV)/bin/pip && echo '✅ yes' || echo '❌ no')"
	@echo ""
	@echo "config.json: $$(test -f config.json && echo '✅ exists' || echo '❌ not found')"
	@echo "overlay_enhanced.py: $$(test -f overlay_enhanced.py && echo '✅ exists' || echo '❌ not found')"
	@echo ""

# Quick start (run without checking)
.PHONY: quick
quick:
	$(PYTHON) overlay.py

# Development mode (with error output)
.PHONY: dev
dev:
	@echo "Running in development mode..."
	$(PYTHON) -u overlay.py

# Show project info
.PHONY: info
info:
	@echo "TFT AI Overlay - Project Information"
	@echo ""
	@echo "Files:"
	@ls -lh *.py | awk '{print "  " $$9, "-", $$5}'
	@echo ""
	@echo "Virtual Environment:"
	@echo "  Location: $(VENV)"
	@echo "  Python: $(PYTHON)"
	@echo ""
	@echo "Documentation:"
	@echo "  - QUICKSTART.md (getting started)"
	@echo "  - README.md (overview)"
	@echo "  - implementation_guide.md (technical details)"
	@echo ""
