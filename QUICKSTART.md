# Quick Start Guide - TFT AI Overlay

## Setup Instructions

### Option 1: Using Virtual Environment (Recommended)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**

   **Windows (CMD):**
   ```bash
   venv\Scripts\activate
   ```

   **Windows (PowerShell):**
   ```bash
   venv\Scripts\Activate.ps1
   ```

   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Using System Python (if allowed)

```bash
pip install -r requirements.txt --user
```

### Option 3: Install Tesseract OCR

**This is REQUIRED for OCR features to work!**

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Note the installation path (usually `C:\Program Files\Tesseract-OCR`)
4. If not in default location, edit `.env` file:
   ```
   TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
   ```

**Linux/WSL:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

## Configure API Key

### Step 1: Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 2: Add Key to .env File

Edit the `.env` file and replace the placeholder:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Important**: The `.env` file is already created and won't be committed to git!

## Run the Application

### Simple Method (Once dependencies are installed):

```bash
python overlay.py
```

### From Virtual Environment:

**Windows:**
```bash
venv\Scripts\activate
python overlay.py
```

**Linux/Mac:**
```bash
source venv/bin/activate
python overlay.py
```

## How to Use

### Method 1: Manual Input (Works Immediately)

1. Launch the overlay: `python overlay.py`
2. Click **"Input State"** button
3. Click **"Load Example"** to see the JSON format
4. Edit the JSON to match your current TFT game
5. Click **"OK"**
6. Click **"Get Hint"** for recommendations

**Example JSON:**
```json
{
  "round": 5,
  "level": 5,
  "gold": 45,
  "current_board": [
    {"unit": "Ahri", "stars": 2, "items": ["Blue Buff"], "position": [0,0]}
  ],
  "bench": ["Kai'Sa"],
  "available_shops": ["Thresh", "Warwick"],
  "synergies": {"Mystic": 2},
  "health": 75,
  "stage": "3-2"
}
```

### Method 2: Screen Capture (Phase 2)

1. Make sure TFT is running
2. Click **"Capture Screen"** - saves screenshot to `captures/` folder
3. Click **"OCR Analyze"** - attempts to read game stats from screen
4. Click **"Get Hint"** for AI recommendations

## Troubleshooting

### "No module named 'dotenv'" or similar errors

**Solution:**
```bash
pip install python-dotenv openai Pillow mss pytesseract numpy
```

### "Could not detect game state" (OCR)

**Causes:**
- Tesseract not installed
- TFT game not visible on screen
- UI elements obscured

**Solutions:**
- Install Tesseract OCR (see above)
- Ensure TFT is in windowed mode and visible
- Set correct TESSERACT_PATH in `.env` if custom install

### "OpenAI API error"

**Causes:**
- API key not set or invalid
- No API credits

**Solutions:**
- Check `.env` file has correct API key
- Verify credits at: https://platform.openai.com/usage
- App will work without API (uses rule-based analysis)

### Virtual environment not activating

**Windows PowerShell error?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

## Testing Without TFT

You can test the app without playing TFT:

1. Run `python overlay.py`
2. Click "Input State"
3. Click "Load Example"
4. Click "OK"
5. Click "Get Hint"

You should see recommendations appear!

## What Works Without API Key?

- ✅ Manual game state input
- ✅ Rule-based recommendations
- ✅ Screen capture
- ✅ OCR analysis
- ❌ AI-enhanced recommendations (requires API key)

## What Works Without Tesseract?

- ✅ Manual game state input
- ✅ Rule-based recommendations
- ✅ Screen capture (saving screenshots)
- ✅ AI-enhanced recommendations
- ❌ OCR analysis (requires Tesseract)

## Minimal Setup (Just to Test)

If you just want to try it out:

1. Install Python packages: `pip install tk python-dotenv`
2. Run: `python overlay.py`
3. Use manual input mode only

## Full Setup (All Features)

1. Install all Python packages: `pip install -r requirements.txt`
2. Install Tesseract OCR
3. Add OpenAI API key to `.env`
4. Run: `python overlay.py`
5. All features available!

## Next Steps

- Read [README.md](README.md) for overview
- Read [implementation_guide.md](implementation_guide.md) for detailed documentation
- Edit `config.json` to add custom recommendation rules
- Try different OpenAI models in `.env` (gpt-3.5-turbo vs gpt-4)

## Need Help?

Check the files:
- **QUICKSTART.md** (this file) - Getting started
- **README.md** - Project overview
- **implementation_guide.md** - Full technical documentation
