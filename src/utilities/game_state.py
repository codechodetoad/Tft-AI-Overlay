import json

class GameState:
    def __init__(self):
        self.round = 0
        self.level = 0
        self.gold = 0
        self.current_board = []
        self.bench = []
        self.available_shops = []
        self.synergies = {}
        self.health = 100
        self.stage = ""
    
    def load_from_dict(self, data):
        """Load game state from dictionary"""
        self.round = data.get("round", 0)
        self.level = data.get("level", 0)
        self.gold = data.get("gold", 0)
        self.current_board = data.get("current_board", [])
        self.bench = data.get("bench", [])
        self.available_shops = data.get("available_shops", [])
        self.synergies = data.get("synergies", {})
        self.health = data.get("health", 100)
        self.stage = data.get("stage", "")
    
    def is_valid(self):
        """Check if game state has valid data"""
        return (
            self.level > 0 and 
            self.gold >= 0 and 
            self.health > 0 and 
            self.stage != ""
        )
    
    def get_display_text(self):
        """Get formatted text for displaying game state"""
        text = f"Stage: {self.stage}\n"
        text += f"Level: {self.level} | Gold: {self.gold} | Health: {self.health}\n\n"
        
        text += "Board:\n"
        for unit in self.current_board:
            items_str = ", ".join(unit.get("items", []))
            text += f"  {unit['unit']} ({unit['stars']}★) - {items_str}\n"
        
        text += "\nSynergies:\n"
        for synergy, count in self.synergies.items():
            text += f"  {synergy}: {count}\n"
        
        text += f"\nShop: {', '.join(self.available_shops)}"
        
        return text