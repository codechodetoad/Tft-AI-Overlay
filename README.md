# TFT Overlay

A comprehensive overlay for Teamfight Tactics with strategic recommendations, computer vision, and meta data integration.

## 🎮 Features

### Phase 1-2: Core Functionality ✅
- Manual game state input (JSON)
- Rule-based strategic recommendations
- Always-on-top overlay window
- Screen capture (WSL2 compatible)
- OCR-based game state detection
- Multi-tab interface (Main, Stats, Comps, Settings)

### Phase 3-5: Advanced Features ✅
- **Database System** - SQLAlchemy ORM for champions, items, augments, compositions
- **Web Scraping** - Live meta data from MetaTFT.com
- **Computer Vision** - Board detection, star recognition, unit positioning
- **Win Probability Calculator** - Heuristic-based placement predictions
- **Positioning Optimizer** - Auto tank/carry/support placement with hex grid
- **Itemization Guide** - Smart item recommendations per champion
- **Economy Tracker** - Interest, leveling, and rolling advice
- **Match History** - Track placements and statistics
- **Composition Library** - Save and load team comps
- **Game Detector** - Auto-detect League client
- **Keyboard Shortcuts** - F1-F4 hotkeys
- **Themes** - Dark, Light, and TFT-themed colors

## 🚀 Quick Start

```bash
# One-time setup
make setup

# Run the overlay
make run
```

## 📦 Installation

### 1. Install Dependencies

```bash
# Create virtual environment and install everything
make setup

# Or manually:
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

### 2. Install Tesseract OCR (Optional - for OCR features)

**Linux/WSL:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki

### 3. Initialize Game Data

```bash
# Update meta data from web
make update-data
```

## 🎯 Usage

### Run the Application

```bash
make run
```

### Features Available

1. **Manual Input** - Click "Input State" → Load example or enter JSON → "Get Hint"
2. **Screen Capture** - Click "Capture Screen" (F3) to save screenshot
3. **OCR Analysis** - Click "OCR Analyze" (F4) to extract game stats
4. **Auto-Updates** - Toggle "Start Auto-Update" for background monitoring
5. **Match History** - Save matches, view stats (Top 4 rate, Win rate)
6. **Comp Library** - Save/load team compositions

### Keyboard Shortcuts

- **F1** - Get Hint
- **F2** - Input State
- **F3** - Capture Screen
- **F4** - OCR Analyze

## 📁 Project Structure

```
src/
├── main/               # Main application
│   ├── overlay.py
│   └── overlay_enhanced.py
├── utilities/          # Core utilities
│   ├── game_state.py
│   ├── analyzer.py
│   ├── screen_capture.py
│   ├── ocr_reader.py
│   └── ...
├── database/          # SQLAlchemy models & manager
├── scrapers/          # Web scraping (MetaTFT)
├── analysis/          # Win calc, positioning, itemization
├── automation/        # Game detection
└── core/             # Master controller

config.json           # Recommendation rules
units.json           # Champion database
requirements.txt     # Dependencies
tft_overlay.py       # Main launcher
Makefile            # Build commands
```

## 🔧 Advanced Features

### Win Probability
Calculates top 1, top 4, and bottom 4 probabilities based on:
- Health, level, gold
- Board strength (cost × stars)
- Stage progression

### Positioning Optimizer
Automatically places units:
- **Tanks** → Front line (rows 0-1)
- **Carries** → Back line corners (row 3)
- **Supports** → Mid line (row 2)

### Itemization Guide
Recommends items based on:
- Champion cost and role
- Available components
- Meta item priorities

### Web Scraping
Auto-updates every 6 hours:
- Meta compositions with win rates
- Augment tier lists (S/A/B/C/D)
- Item priority rankings

## 📊 Statistics

- **Total Lines of Code**: ~4,000
- **Modules**: 25+
- **Phases Complete**: 1-5 (100%)
- **Dependencies**: 12

## 🛠️ Commands

```bash
make run          # Run the overlay
make setup        # One-time setup
make install      # Install/update dependencies
make test         # Test installation
make update-data  # Update meta data from web
make clean        # Remove cache files
make info         # Show project info
```

## ⚙️ Configuration

### Custom Rules

Edit `config.json`:
```json
{
  "rules": [
    {
      "condition": {"field": "level", "operator": "eq", "value": 8},
      "recommendation": "At level 8, roll for 5-cost units"
    }
  ]
}
```

### Database

All data stored in `data/tft_overlay.db`:
- Champions, items, augments, compositions
- Match history
- Champion templates (for recognition)

## 🐛 Troubleshooting

### ModuleNotFoundError
```bash
make install
```

### OCR Not Working
- Install Tesseract: `sudo apt-get install tesseract-ocr`
- Check TFT is visible on screen
- Verify game resolution (1080p+ recommended)

### WSL2 Screen Capture Issues
- Overlay uses PowerShell for WSL2 screen capture
- Ensure Windows PowerShell is accessible
- Game must be in windowed/borderless mode

## 🚧 Known Limitations

- Champion recognition requires manual template creation (~1-2 hours)
- OCR accuracy varies by screen resolution
- Web scraping depends on site structure (has fallbacks)

## 📚 Documentation

- **implementation_guide.md** - Technical implementation details
- **Inline code comments** - Detailed function documentation

## 🔐 Security

- `.gitignore` protects sensitive files
- Database and cache files excluded from git
- No API keys required (features degrade gracefully)

## 🎓 Requirements

- Python 3.7+
- Tesseract OCR (optional)
- 1920x1080+ resolution (recommended)

## 📄 License

Educational / Personal Use

## ⚖️ Disclaimer

This tool is not affiliated with Riot Games. Use responsibly and in accordance with TFT Terms of Service.

---

**Current Version**: Phase 5 Complete
**Status**: Fully Functional
**Platform**: Linux, macOS, WSL2, Windows
