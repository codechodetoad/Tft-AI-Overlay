import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import json
from utilities.game_state import GameState
from utilities.analyzer import Analyzer
from utilities.screen_capture import ScreenCapture
from utilities.ocr_reader import OCRReader
from utilities.board_detector import BoardDetector
from utilities.auto_updater import AutoUpdater
from utilities.advanced_features import MatchHistory, CompLibrary, HotkeyManager, ThemeManager, EconomyTracker

class TFTOverlayEnhanced:
    def __init__(self, root):
        self.root = root
        self.root.title("TFT Overlay - Phase 5")
        self.root.geometry("400x600")
        self.root.attributes("-topmost", True)
        
        # Position window
        self.root.geometry("+{}+{}".format(
            root.winfo_screenwidth() - 420,
            root.winfo_screenheight() - 620
        ))
        
        # Initialize components
        self.game_state = GameState()
        self.analyzer = Analyzer()
        self.screen_capture = ScreenCapture()
        self.ocr_reader = OCRReader()
        self.board_detector = BoardDetector()
        
        # Phase 4: Auto-updater
        self.auto_updater = AutoUpdater(self.game_state, self.on_auto_update)
        
        # Phase 5: Advanced features
        self.match_history = MatchHistory()
        self.comp_library = CompLibrary()
        self.theme_manager = ThemeManager()
        self.economy_tracker = EconomyTracker()
        
        # Create UI
        self.create_widgets()
        
        # Phase 5: Hotkeys
        self.hotkey_manager = HotkeyManager(self)
        self.hotkey_manager.bind_hotkeys(root)
        
    def create_widgets(self):
        # Apply theme
        theme = self.theme_manager.get_theme()
        self.root.configure(bg=theme["bg"])
        
        # Title
        title = ttk.Label(self.root, text="TFT Overlay Pro", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")
        self.create_main_tab()
        
        # Stats tab
        self.stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_tab, text="Stats")
        self.create_stats_tab()
        
        # Comps tab
        self.comps_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.comps_tab, text="Comps")
        self.create_comps_tab()
        
        # Settings tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        self.create_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_main_tab(self):
        # Game state display
        self.state_display = scrolledtext.ScrolledText(
            self.main_tab, width=45, height=10, wrap=tk.WORD
        )
        self.state_display.pack(padx=10, pady=5)
        self.state_display.insert(tk.END, "No game state loaded")
        self.state_display.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(self.main_tab)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Get Hint (F1)", command=self.get_hint).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Input State (F2)", command=self.input_state).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Capture (F3)", command=self.capture_screen).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="OCR (F4)", command=self.ocr_analyze).grid(row=1, column=1, padx=5, pady=5)
        
        # Auto-update control
        auto_frame = ttk.Frame(self.main_tab)
        auto_frame.pack(pady=5)
        self.auto_btn = ttk.Button(auto_frame, text="Start Auto-Update", command=self.toggle_auto_update)
        self.auto_btn.pack()
        
        # Recommendations
        ttk.Label(self.main_tab, text="Recommendations:").pack(pady=5)
        self.recommendation = scrolledtext.ScrolledText(
            self.main_tab, width=45, height=8, wrap=tk.WORD
        )
        self.recommendation.pack(padx=10, pady=5)
        self.recommendation.insert(tk.END, "Click 'Get Hint' for recommendations")
        self.recommendation.config(state=tk.DISABLED)
        
    def create_stats_tab(self):
        ttk.Label(self.stats_tab, text="Match History", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.stats_display = scrolledtext.ScrolledText(self.stats_tab, width=45, height=15, wrap=tk.WORD)
        self.stats_display.pack(padx=10, pady=5)
        
        btn_frame = ttk.Frame(self.stats_tab)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Refresh Stats", command=self.refresh_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save Match", command=self.save_match).pack(side=tk.LEFT, padx=5)
        
        self.refresh_stats()
        
    def create_comps_tab(self):
        ttk.Label(self.comps_tab, text="Saved Compositions", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Comp list
        self.comp_listbox = tk.Listbox(self.comps_tab, height=10)
        self.comp_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = ttk.Frame(self.comps_tab)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Save Current", command=self.save_comp).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load", command=self.load_comp).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_comp).pack(side=tk.LEFT, padx=5)
        
        self.refresh_comp_list()
        
    def create_settings_tab(self):
        ttk.Label(self.settings_tab, text="Settings", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Auto-update interval
        ttk.Label(self.settings_tab, text="Auto-update interval (seconds):").pack(pady=5)
        self.interval_var = tk.StringVar(value="3")
        ttk.Entry(self.settings_tab, textvariable=self.interval_var, width=10).pack(pady=5)
        ttk.Button(self.settings_tab, text="Apply", command=self.apply_settings).pack(pady=5)
        
        # Theme selection
        ttk.Label(self.settings_tab, text="Theme:").pack(pady=5)
        theme_frame = ttk.Frame(self.settings_tab)
        theme_frame.pack(pady=5)
        for theme_name in ["dark", "light", "tft"]:
            ttk.Button(theme_frame, text=theme_name.capitalize(), 
                      command=lambda t=theme_name: self.change_theme(t)).pack(side=tk.LEFT, padx=5)
        
    def get_hint(self):
        self.status_var.set("Analyzing...")
        self.root.update()
        
        if not self.game_state.is_valid():
            messagebox.showwarning("No Game State", "Please input a valid game state first")
            self.status_var.set("No game state")
            return
        
        hint = self.analyzer.analyze(self.game_state)
        
        # Add economy advice
        economy_advice = self.economy_tracker.get_economy_advice(
            self.game_state.gold, self.game_state.level
        )
        if economy_advice:
            hint += "\n\nEconomy:\n" + "\n".join(f"- {a}" for a in economy_advice)
        
        self.recommendation.config(state=tk.NORMAL)
        self.recommendation.delete(1.0, tk.END)
        self.recommendation.insert(tk.END, hint)
        self.recommendation.config(state=tk.DISABLED)
        
        self.status_var.set("Hint generated")
        
    def input_state(self):
        dialog = GameStateDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                state_data = json.loads(dialog.result)
                self.game_state.load_from_dict(state_data)
                
                self.state_display.config(state=tk.NORMAL)
                self.state_display.delete(1.0, tk.END)
                self.state_display.insert(tk.END, self.game_state.get_display_text())
                self.state_display.config(state=tk.DISABLED)
                
                self.status_var.set("Game state loaded")
            except json.JSONDecodeError:
                messagebox.showerror("Invalid JSON", "Please enter valid JSON data")
                
    def capture_screen(self):
        self.status_var.set("Capturing...")
        try:
            img = self.screen_capture.capture_full_screen()
            filepath = self.screen_capture.save_capture(img)
            self.status_var.set(f"Captured: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def ocr_analyze(self):
        self.status_var.set("OCR analyzing...")
        try:
            img = self.screen_capture.capture_full_screen()
            stats = self.ocr_reader.read_game_stats(img)
            
            if stats['level'] > 0:
                self.game_state.level = stats['level']
                self.game_state.gold = stats['gold']
                self.game_state.health = stats['health']
                self.game_state.stage = stats['stage']
                
                self.state_display.config(state=tk.NORMAL)
                self.state_display.delete(1.0, tk.END)
                self.state_display.insert(tk.END, f"OCR Detected:\n")
                self.state_display.insert(tk.END, f"Stage: {stats['stage']}\n")
                self.state_display.insert(tk.END, f"Level: {stats['level']}\n")
                self.state_display.insert(tk.END, f"Gold: {stats['gold']}\n")
                self.state_display.insert(tk.END, f"Health: {stats['health']}\n")
                self.state_display.config(state=tk.DISABLED)
                
                self.status_var.set("OCR complete")
            else:
                messagebox.showwarning("OCR Failed", "Could not detect game state")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def toggle_auto_update(self):
        if self.auto_updater.is_running():
            self.auto_updater.stop()
            self.auto_btn.config(text="Start Auto-Update")
            self.status_var.set("Auto-update stopped")
        else:
            self.auto_updater.start()
            self.auto_btn.config(text="Stop Auto-Update")
            self.status_var.set("Auto-update started")
            
    def on_auto_update(self):
        """Callback when auto-updater detects changes"""
        self.state_display.config(state=tk.NORMAL)
        self.state_display.delete(1.0, tk.END)
        self.state_display.insert(tk.END, self.game_state.get_display_text())
        self.state_display.config(state=tk.DISABLED)
        
    def refresh_stats(self):
        stats = self.match_history.get_stats()
        
        self.stats_display.config(state=tk.NORMAL)
        self.stats_display.delete(1.0, tk.END)
        self.stats_display.insert(tk.END, "=== Match Statistics ===\n\n")
        self.stats_display.insert(tk.END, f"Total Games: {stats.get('total_games', 0)}\n")
        if stats['total_games'] > 0:
            self.stats_display.insert(tk.END, f"Avg Placement: {stats.get('avg_placement', 0):.2f}\n")
            self.stats_display.insert(tk.END, f"Top 4 Rate: {stats.get('top_4_rate', 0):.1f}%\n")
            self.stats_display.insert(tk.END, f"Win Rate: {stats.get('win_rate', 0):.1f}%\n")
        self.stats_display.config(state=tk.DISABLED)
        
    def save_match(self):
        placement = simpledialog.askinteger("Save Match", "Enter placement (1-8):", minvalue=1, maxvalue=8)
        if placement:
            self.match_history.save_match(self.game_state, placement)
            self.refresh_stats()
            messagebox.showinfo("Saved", "Match saved to history")
            
    def save_comp(self):
        name = simpledialog.askstring("Save Comp", "Enter composition name:")
        if name:
            self.comp_library.save_comp(name, self.game_state)
            self.refresh_comp_list()
            messagebox.showinfo("Saved", f"Composition '{name}' saved")
            
    def load_comp(self):
        selection = self.comp_listbox.curselection()
        if selection:
            name = self.comp_listbox.get(selection[0])
            comp = self.comp_library.load_comp(name)
            if comp:
                self.game_state.current_board = comp['board']
                self.game_state.synergies = comp['synergies']
                self.game_state.level = comp['level']
                
                self.state_display.config(state=tk.NORMAL)
                self.state_display.delete(1.0, tk.END)
                self.state_display.insert(tk.END, self.game_state.get_display_text())
                self.state_display.config(state=tk.DISABLED)
                
                messagebox.showinfo("Loaded", f"Loaded '{name}'")
                
    def delete_comp(self):
        selection = self.comp_listbox.curselection()
        if selection:
            name = self.comp_listbox.get(selection[0])
            if messagebox.askyesno("Delete", f"Delete '{name}'?"):
                self.comp_library.delete_comp(name)
                self.refresh_comp_list()
                
    def refresh_comp_list(self):
        self.comp_listbox.delete(0, tk.END)
        for comp in self.comp_library.list_comps():
            self.comp_listbox.insert(tk.END, comp)
            
    def apply_settings(self):
        try:
            interval = float(self.interval_var.get())
            self.auto_updater.set_update_interval(interval)
            messagebox.showinfo("Applied", "Settings applied")
        except ValueError:
            messagebox.showerror("Error", "Invalid interval value")
            
    def change_theme(self, theme_name):
        theme = self.theme_manager.apply_theme(self.root, theme_name)
        messagebox.showinfo("Theme", f"Theme changed to {theme_name}")

class GameStateDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Input Game State")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text="Enter game state as JSON:").pack(pady=5)
        ttk.Button(self.dialog, text="Load Example", command=self.load_example).pack(pady=5)
        
        self.text_input = scrolledtext.ScrolledText(self.dialog, width=60, height=20, wrap=tk.WORD)
        self.text_input.pack(padx=10, pady=5)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
    
    def load_example(self):
        example_state = {
            "round": 5, "level": 5, "gold": 45,
            "current_board": [
                {"unit": "Ahri", "stars": 2, "items": ["Blue Buff"], "position": [0,0]}
            ],
            "bench": ["Kai'Sa"],
            "available_shops": ["Thresh", "Warwick", "Lulu"],
            "synergies": {"Mystic": 2},
            "health": 75,
            "stage": "3-2"
        }
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(tk.END, json.dumps(example_state, indent=2))
    
    def ok_clicked(self):
        self.result = self.text_input.get(1.0, tk.END)
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TFTOverlayEnhanced(root)
    root.mainloop()
