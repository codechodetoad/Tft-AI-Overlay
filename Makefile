# Makefile for TFT Overlay

PYTHON = venv/bin/python3
VENV = venv

.PHONY: help
help:
	@echo "TFT Overlay - Available Commands:"
	@echo ""
	@echo "  make run          - Run the Phase 5 overlay"
	@echo "  make setup        - Initial setup (create venv + install deps)"
	@echo "  make install      - Install/update dependencies"
	@echo "  make test         - Test the installation"
	@echo "  make clean        - Remove cache and temp files"
	@echo "  make update-data  - Update web-scraped TFT data"
	@echo ""

.PHONY: run
run:
	@echo "Starting TFT Overlay..."
	$(PYTHON) tft_overlay.py

.PHONY: setup
setup:
	@echo "Setting up TFT Overlay..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
	fi
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo ""
	@echo "✅ Setup complete!"
	@echo "Run: make run"

.PHONY: install
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: test
test:
	@echo "Testing installation..."
	@$(PYTHON) --version
	@echo ""
	@$(PYTHON) -c "import PIL; print('✅ Pillow')"
	@$(PYTHON) -c "import mss; print('✅ mss')"
	@$(PYTHON) -c "import pytesseract; print('✅ pytesseract')"
	@$(PYTHON) -c "import cv2; print('✅ opencv')"
	@$(PYTHON) -c "import numpy; print('✅ numpy')"
	@$(PYTHON) -c "import requests; print('✅ requests')"
	@$(PYTHON) -c "import bs4; print('✅ beautifulsoup4')"

.PHONY: clean
clean:
	@echo "Cleaning..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf tmp/

.PHONY: update-data
update-data:
	@echo "Updating TFT data from web..."
	$(PYTHON) -c "from src.utilities.web_scraper import TFTDataScraper; s = TFTDataScraper(); s.update_all_data()"

.PHONY: info
info:
	@echo "TFT Overlay - Project Structure"
	@echo ""
	@echo "Main Application:"
	@ls -lh src/main/*.py 2>/dev/null | awk '{print "  " $$9, "-", $$5}'
	@echo ""
	@echo "Utilities:"
	@ls -lh src/utilities/*.py 2>/dev/null | awk '{print "  " $$9, "-", $$5}'
