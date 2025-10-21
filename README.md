# TFT AI Overlay

An AI-powered overlay for Teamfight Tactics that provides strategic recommendations in real-time.

## Features

### Phase 1 (MVP) ✅
- Manual game state input
- Rule-based strategic recommendations
- Always-on-top overlay window
- JSON-based configuration

### Phase 2 (Advanced) ✅
- Screen capture functionality
- OCR-based game state detection
- OpenAI GPT integration for AI recommendations
- Environment variable management for API keys

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

**Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki

**Linux**:
```bash
sudo apt-get install tesseract-ocr
```

### 3. Configure API Key

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

   Get your API key from: https://platform.openai.com/api-keys

### 4. Run the Application

```bash
python overlay.py
```

## Usage

### Manual Mode
1. Click "Input State" button
2. Enter your game state as JSON (or click "Load Example")
3. Click "Get Hint" for AI recommendations

### Automated Mode (Phase 2)
1. Click "Capture Screen" to screenshot the game
2. Click "OCR Analyze" to extract game stats automatically
3. Click "Get Hint" for AI-powered recommendations

## Files Created

- **[.gitignore](.gitignore)** - Protects your API keys from being committed
- **[.env](.env)** - Your environment variables (add your API key here)
- **[.env.example](.env.example)** - Template for environment variables
- **[requirements.txt](requirements.txt)** - Python dependencies
- **[implementation_guide.md](implementation_guide.md)** - Comprehensive development guide

## New Phase 2 Files

- **[screen_capture.py](screen_capture.py)** - Screen capture functionality
- **[ocr_reader.py](ocr_reader.py)** - OCR text extraction
- **[ai_analyzer.py](ai_analyzer.py)** - AI-enhanced analyzer

## Project Structure

```
Tft-AI-Overlay/
├── .env                    # Your API keys (DO NOT COMMIT)
├── .env.example            # Template
├── .gitignore              # Protects sensitive files
├── requirements.txt        # Dependencies
│
├── config.json            # Recommendation rules
├── units.json             # Unit data
│
├── game_state.py          # Game state model
├── analyzer.py            # Rule-based analyzer
├── ai_analyzer.py         # AI analyzer (NEW)
├── screen_capture.py      # Screen capture (NEW)
├── ocr_reader.py          # OCR functionality (NEW)
└── overlay.py             # Main application
```

## Configuration

### Adding API Key

Edit `.env`:
```bash
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4
```

### Adding Custom Rules

Edit `config.json`:
```json
{
  "rules": [
    {
      "condition": {
        "field": "level",
        "operator": "eq",
        "value": 8
      },
      "recommendation": "At level 8, start rolling for 5-cost units"
    }
  ]
}
```

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Could not detect game state" (OCR)
- Ensure Tesseract is installed
- Make sure TFT is visible on screen
- Try higher game resolution

### "OpenAI API error"
- Check API key in `.env`
- Verify you have credits: https://platform.openai.com/usage

## Documentation

See [implementation_guide.md](implementation_guide.md) for:
- Detailed architecture
- Phase-by-phase implementation details
- API usage and costs
- Advanced configuration
- Future roadmap

## Security

- `.env` file is automatically excluded from git
- Never commit API keys to version control
- The `.gitignore` file protects sensitive data

## Requirements

- Python 3.7+
- Tesseract OCR
- OpenAI API key (optional, falls back to rule-based analysis)

## License

Educational / Personal Use

## Disclaimer

This tool is not affiliated with Riot Games. Use responsibly and in accordance with TFT Terms of Service.
