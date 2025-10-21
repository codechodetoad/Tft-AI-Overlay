#!/bin/bash
# Simple run script for TFT AI Overlay

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}TFT AI Overlay${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found!${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv

    echo "Installing dependencies..."
    venv/bin/pip install --upgrade pip
    venv/bin/pip install -r requirements.txt

    echo -e "${GREEN}✅ Setup complete!${NC}"
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Using defaults...${NC}"
fi

# Run the application
echo -e "${GREEN}Starting TFT AI Overlay...${NC}"
venv/bin/python overlay.py
