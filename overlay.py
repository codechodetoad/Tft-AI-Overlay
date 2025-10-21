import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import json
from game_state import GameState
from analyzer import Analyzer
from ai_analyzer import AIAnalyzer
from screen_capture import ScreenCapture
from ocr_reader import OCRReader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TFTOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("TFT AI Overlay - MVP")
        self.root.geometry("300x400")
        self.root.attributes("-topmost", True)  # Keep overlay on top
        
        # Position window at bottom-right
        self.root.geometry("+{}+{}".format(
            root.winfo_screenwidth() - 320,
            root.winfo_screenheight() - 420
        ))
        
        # Initialize game state and analyzers
        self.game_state = GameState()
        self.analyzer = Analyzer()  # Rule-based analyzer
        self.ai_analyzer = AIAnalyzer()  # AI-enhanced analyzer
        self.screen_capture = ScreenCapture()
        self.ocr_reader = OCRReader()

        # Track which analyzer to use
        self.use_ai = os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here'
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="TFT AI Overlay", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Current game state display
        self.state_display = scrolledtext.ScrolledText(
            self.root, width=35, height=10, wrap=tk.WORD
        )
        self.state_display.pack(padx=10, pady=5)
        self.state_display.insert(tk.END, "No game state loaded")
        self.state_display.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        hint_btn = ttk.Button(
            button_frame, text="Get Hint", command=self.get_hint
        )
        hint_btn.pack(side=tk.LEFT, padx=5)

        input_btn = ttk.Button(
            button_frame, text="Input State", command=self.input_state
        )
        input_btn.pack(side=tk.LEFT, padx=5)

        # Second row of buttons for Phase 2 features
        button_frame2 = ttk.Frame(self.root)
        button_frame2.pack(pady=5)

        capture_btn = ttk.Button(
            button_frame2, text="Capture Screen", command=self.capture_screen
        )
        capture_btn.pack(side=tk.LEFT, padx=5)

        ocr_btn = ttk.Button(
            button_frame2, text="OCR Analyze", command=self.ocr_analyze
        )
        ocr_btn.pack(side=tk.LEFT, padx=5)
        
        # Recommendation display
        self.recommendation = scrolledtext.ScrolledText(
            self.root, width=35, height=8, wrap=tk.WORD
        )
        self.recommendation.pack(padx=10, pady=5)
        self.recommendation.insert(tk.END, "Click 'Get Hint' for recommendations")
        self.recommendation.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def get_hint(self):
        """Generate and display a hint based on current game state"""
        self.status_var.set("Analyzing...")
        self.root.update()

        if not self.game_state.is_valid():
            messagebox.showwarning("No Game State", "Please input a valid game state first")
            self.status_var.set("No game state")
            return

        # Get recommendation from analyzer (use AI if available)
        if self.use_ai:
            hint = self.ai_analyzer.analyze(self.game_state)
        else:
            hint = self.analyzer.analyze(self.game_state)

        # Display recommendation
        self.recommendation.config(state=tk.NORMAL)
        self.recommendation.delete(1.0, tk.END)
        self.recommendation.insert(tk.END, hint)
        self.recommendation.config(state=tk.DISABLED)

        self.status_var.set("Hint generated (AI)" if self.use_ai else "Hint generated (Rules)")
    
    def input_state(self):
        """Open dialog to input game state"""
        dialog = GameStateDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                # Parse JSON input
                state_data = json.loads(dialog.result)
                self.game_state.load_from_dict(state_data)
                
                # Update display
                self.state_display.config(state=tk.NORMAL)
                self.state_display.delete(1.0, tk.END)
                self.state_display.insert(tk.END, self.game_state.get_display_text())
                self.state_display.config(state=tk.DISABLED)
                
                self.status_var.set("Game state loaded")
            except json.JSONDecodeError:
                messagebox.showerror("Invalid JSON", "Please enter valid JSON data")
                self.status_var.set("Error loading state")

    def capture_screen(self):
        """Capture the game screen"""
        self.status_var.set("Capturing screen...")
        self.root.update()

        try:
            # Capture the screen
            img = self.screen_capture.capture_full_screen()

            # Save the capture
            filepath = self.screen_capture.save_capture(img)

            self.status_var.set(f"Screen captured: {filepath}")
            messagebox.showinfo("Capture Successful", f"Screenshot saved to:\n{filepath}\n\nUse 'OCR Analyze' to extract game state.")

        except Exception as e:
            messagebox.showerror("Capture Error", f"Failed to capture screen:\n{str(e)}")
            self.status_var.set("Capture failed")

    def ocr_analyze(self):
        """Analyze game state using OCR from screen capture"""
        self.status_var.set("Performing OCR analysis...")
        self.root.update()

        try:
            # Capture the screen first
            img = self.screen_capture.capture_full_screen()

            # Extract game stats using OCR
            game_stats = self.ocr_reader.read_game_stats(img)

            # Update game state with OCR data
            if game_stats['level'] > 0:
                self.game_state.level = game_stats['level']
                self.game_state.gold = game_stats['gold']
                self.game_state.health = game_stats['health']
                self.game_state.stage = game_stats['stage']

                # Update display
                self.state_display.config(state=tk.NORMAL)
                self.state_display.delete(1.0, tk.END)
                self.state_display.insert(tk.END, f"OCR Detected State:\n")
                self.state_display.insert(tk.END, f"Stage: {game_stats['stage']}\n")
                self.state_display.insert(tk.END, f"Level: {game_stats['level']}\n")
                self.state_display.insert(tk.END, f"Gold: {game_stats['gold']}\n")
                self.state_display.insert(tk.END, f"Health: {game_stats['health']}\n\n")
                self.state_display.insert(tk.END, "Note: Manual refinement may be needed.\n")
                self.state_display.insert(tk.END, "Use 'Input State' to add board and synergies.")
                self.state_display.config(state=tk.DISABLED)

                self.status_var.set("OCR analysis complete")
                messagebox.showinfo("OCR Complete", "Basic stats extracted. Please manually add board composition and synergies using 'Input State' for best results.")
            else:
                messagebox.showwarning("OCR Failed", "Could not detect game state. Make sure TFT is visible on screen.\n\nTips:\n- Game should be in focus\n- Stats should be clearly visible\n- Try adjusting game resolution")
                self.status_var.set("OCR failed to detect state")

        except Exception as e:
            messagebox.showerror("OCR Error", f"Failed to analyze screen:\n{str(e)}")
            self.status_var.set("OCR analysis failed")

class GameStateDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Input Game State")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Instructions
        instructions = ttk.Label(
            self.dialog, 
            text="Enter your game state as JSON. See example below:",
            font=("Arial", 10)
        )
        instructions.pack(pady=5)
        
        # Example button
        example_btn = ttk.Button(
            self.dialog, 
            text="Load Example", 
            command=self.load_example
        )
        example_btn.pack(pady=5)
        
        # Text input
        self.text_input = scrolledtext.ScrolledText(
            self.dialog, width=60, height=20, wrap=tk.WORD
        )
        self.text_input.pack(padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ok_btn = ttk.Button(
            button_frame, text="OK", command=self.ok_clicked
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(
            button_frame, text="Cancel", command=self.cancel_clicked
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def load_example(self):
        """Load example game state into text input"""
        example_state = {
            "round": 5,
            "level": 5,
            "gold": 45,
            "current_board": [
                {"unit": "Ahri", "stars": 1, "items": ["Blue Buff"], "position": [0,0]},
                {"unit": "Viktor", "stars": 2, "items": ["Morellonomicon"], "position": [1,0]},
                {"unit": "Syndra", "stars": 1, "items": [], "position": [2,0]}
            ],
            "bench": ["Kai'Sa", "Ashe"],
            "available_shops": ["Kai'Sa", "Thresh", "Warwick", "Lulu", "Vayne"],
            "synergies": {"Mystic": 2, "Invoker": 2},
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
    app = TFTOverlay(root)
    root.mainloop()