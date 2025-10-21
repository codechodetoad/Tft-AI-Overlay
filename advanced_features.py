import json
import os
from datetime import datetime

class MatchHistory:
    """Phase 5: Track match history and performance"""

    def __init__(self, history_file="match_history.json"):
        self.history_file = history_file
        self.matches = self._load_history()

    def _load_history(self):
        """Load match history from file"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_match(self, game_state, placement, comp_name=""):
        """Save a completed match"""
        match_data = {
            "timestamp": datetime.now().isoformat(),
            "placement": placement,
            "comp_name": comp_name,
            "final_level": game_state.level,
            "board": game_state.current_board,
            "synergies": game_state.synergies
        }

        self.matches.append(match_data)
        self._save_history()

    def _save_history(self):
        """Save history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.matches, f, indent=2)

    def get_stats(self):
        """Get performance statistics"""
        if not self.matches:
            return {"total_games": 0}

        placements = [m['placement'] for m in self.matches if 'placement' in m]

        return {
            "total_games": len(self.matches),
            "avg_placement": sum(placements) / len(placements) if placements else 0,
            "top_4_rate": len([p for p in placements if p <= 4]) / len(placements) * 100 if placements else 0,
            "win_rate": len([p for p in placements if p == 1]) / len(placements) * 100 if placements else 0
        }


class CompLibrary:
    """Phase 5: Save and load compositions"""

    def __init__(self, library_file="comp_library.json"):
        self.library_file = library_file
        self.comps = self._load_library()

    def _load_library(self):
        """Load comp library from file"""
        if os.path.exists(self.library_file):
            with open(self.library_file, 'r') as f:
                return json.load(f)
        return {}

    def save_comp(self, name, game_state, notes=""):
        """Save current board as a composition"""
        self.comps[name] = {
            "board": game_state.current_board,
            "synergies": game_state.synergies,
            "level": game_state.level,
            "notes": notes,
            "saved_at": datetime.now().isoformat()
        }

        self._save_library()

    def load_comp(self, name):
        """Load a saved composition"""
        return self.comps.get(name)

    def delete_comp(self, name):
        """Delete a composition"""
        if name in self.comps:
            del self.comps[name]
            self._save_library()

    def list_comps(self):
        """List all saved compositions"""
        return list(self.comps.keys())

    def _save_library(self):
        """Save library to file"""
        with open(self.library_file, 'w') as f:
            json.dump(self.comps, f, indent=2)


class HotkeyManager:
    """Phase 5: Keyboard shortcuts"""

    def __init__(self, overlay):
        self.overlay = overlay
        self.hotkeys = {
            '<F1>': self.overlay.get_hint,
            '<F2>': self.overlay.input_state,
            '<F3>': self.overlay.capture_screen,
            '<F4>': self.overlay.ocr_analyze
        }

    def bind_hotkeys(self, root):
        """Bind hotkeys to root window"""
        for key, callback in self.hotkeys.items():
            root.bind(key, lambda e, cb=callback: cb())

    def add_hotkey(self, key, callback):
        """Add a custom hotkey"""
        self.hotkeys[key] = callback


class ThemeManager:
    """Phase 5: Customizable overlay themes"""

    def __init__(self):
        self.themes = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "button_bg": "#3a3a3a",
                "button_fg": "#ffffff",
                "accent": "#007acc"
            },
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "button_bg": "#e0e0e0",
                "button_fg": "#000000",
                "accent": "#0066cc"
            },
            "tft": {
                "bg": "#0f2027",
                "fg": "#ffd700",
                "button_bg": "#203a43",
                "button_fg": "#ffd700",
                "accent": "#2c5364"
            }
        }

        self.current_theme = "dark"

    def get_theme(self, name=None):
        """Get theme colors"""
        theme_name = name or self.current_theme
        return self.themes.get(theme_name, self.themes["dark"])

    def apply_theme(self, root, theme_name):
        """Apply theme to tkinter window"""
        theme = self.get_theme(theme_name)
        self.current_theme = theme_name

        root.configure(bg=theme["bg"])

        # Return theme for widget configuration
        return theme


class EconomyTracker:
    """Phase 5: Track gold economy and interest"""

    def __init__(self):
        self.gold_history = []
        self.interest_earned = 0

    def track_gold(self, current_gold, round_num):
        """Track gold over time"""
        self.gold_history.append({
            "round": round_num,
            "gold": current_gold,
            "timestamp": datetime.now().isoformat()
        })

        # Calculate potential interest
        interest = min(current_gold // 10, 5)
        return interest

    def get_economy_advice(self, current_gold, current_level):
        """Provide economy-specific advice"""
        advice = []

        # Interest breakpoints
        if current_gold < 50:
            next_breakpoint = ((current_gold // 10) + 1) * 10
            needed = next_breakpoint - current_gold
            advice.append(f"Need {needed}g for next interest breakpoint")

        # Leveling costs
        level_costs = {4: 4, 5: 8, 6: 20, 7: 36, 8: 56, 9: 80}
        if current_level in level_costs:
            cost = level_costs[current_level]
            if current_gold >= cost:
                advice.append(f"Can afford to level ({cost}g)")

        # Rolling cost
        if current_gold >= 2:
            rolls_available = current_gold // 2
            advice.append(f"Can roll {rolls_available} times")

        return advice
