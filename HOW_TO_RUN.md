# How to Run TFT AI Overlay

## 🎯 The Easiest Ways to Run

### Method 1: Using Makefile (RECOMMENDED)

```bash
# First time setup (only need to do once)
make setup

# Every time you want to run the app
make run
```

**Other useful make commands:**
```bash
make test              # Test if everything is installed correctly
make ocr-test          # Test Tesseract OCR
make install-tesseract # Install Tesseract on Ubuntu/WSL
make help              # See all available commands
```

### Method 2: Using the Run Script

```bash
# Just run this - it auto-creates venv if needed
./run.sh
```

### Method 3: Direct Command (What You Discovered)

```bash
# This works because it uses the venv's Python directly
venv/bin/python overlay.py
```

## 🤔 Why `overlay.py` Alone Doesn't Work

When you run just `overlay.py` or `python overlay.py`, it uses your system Python, which doesn't have the packages installed.

The virtual environment (`venv/`) has its own Python with all the packages installed. You need to either:

1. **Activate the venv first:**
   ```bash
   source venv/bin/activate  # Now you're "inside" the venv
   python overlay.py         # This now works!
   ```

2. **Use the venv Python directly:**
   ```bash
   venv/bin/python overlay.py  # What you discovered!
   ```

3. **Use a helper (Make/script) that does it for you:**
   ```bash
   make run    # Automatically uses venv/bin/python
   ./run.sh    # Same thing
   ```

## 📊 Full Command Reference

### Setup Commands (Run Once)

```bash
# Option 1: Using Make
make setup

# Option 2: Manual
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### Run Commands (Daily Use)

```bash
# Easiest
make run

# Or
./run.sh

# Or activate venv first
source venv/bin/activate
python overlay.py

# Or use full path
venv/bin/python overlay.py
```

### Optional: Install Tesseract for OCR

```bash
# On Ubuntu/WSL
sudo apt-get install tesseract-ocr

# Or using Make
make install-tesseract

# Test it
make ocr-test
```

### Optional: Add OpenAI API Key for AI

```bash
# Edit the .env file
nano .env

# Replace this line:
OPENAI_API_KEY=your_openai_api_key_here

# With your actual key from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-abc123...
```

## 🔍 Troubleshooting

### "Command 'make' not found"

Install make:
```bash
sudo apt-get install make
```

Then use `make run`

### "Permission denied: ./run.sh"

Make it executable:
```bash
chmod +x run.sh
./run.sh
```

### "venv/bin/python: No such file or directory"

Create the venv first:
```bash
make venv
make install
```

Or just:
```bash
make setup
```

### Still having issues?

Check what's wrong:
```bash
make check-env
make test
```

## 📝 Summary

**For your specific situation, the BEST options are:**

1. **Use Make (if you have it):**
   ```bash
   make run
   ```

2. **Use the run script:**
   ```bash
   ./run.sh
   ```

3. **Use the full path (what works for you now):**
   ```bash
   venv/bin/python overlay.py
   ```

All three methods do the same thing - they use the Python from your virtual environment!

## 🎮 Quick Test Run

Try this to test everything:

```bash
# Setup
make setup

# Run
make run

# Should open the overlay window!
# Click "Input State" → "Load Example" → "OK" → "Get Hint"
```

If that works, you're all set! 🎉
