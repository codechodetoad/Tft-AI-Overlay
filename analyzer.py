import json

class Analyzer:
    def __init__(self):
        # Load configuration
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        
        # Load unit data
        with open('units.json', 'r') as f:
            self.units_data = json.load(f)
    
    def analyze(self, game_state):
        """Analyze game state and return recommendation"""
        recommendations = []
        
        # Check each rule in config
        for rule in self.config["rules"]:
            if self._evaluate_condition(rule["condition"], game_state):
                recommendations.append(rule["recommendation"])
        
        # Generate final recommendation text
        if not recommendations:
            return "No specific recommendations for current state."
        
        result = "Recommendations:\n\n"
        for i, rec in enumerate(recommendations, 1):
            result += f"{i}. {rec}\n"
        
        # Add additional analysis
        result += "\nAdditional Analysis:\n"
        
        # Gold management advice
        if game_state.gold > 50:
            result += "- You have plenty of gold. Consider leveling up.\n"
        elif game_state.gold < 30:
            result += "- Low on gold. Avoid rolling unless necessary.\n"
        
        # Health advice
        if game_state.health < 30:
            result += "- Critical health! Focus on board strength.\n"
        elif game_state.health > 80:
            result += "- Good health. You can focus on economy.\n"
        
        # Synergy advice
        strong_synergies = [s for s, c in game_state.synergies.items() if c >= 3]
        if strong_synergies:
            result += f"- Strong synergies: {', '.join(strong_synergies)}\n"
        
        return result
    
    def _evaluate_condition(self, condition, game_state):
        """Evaluate a single condition against game state"""
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]
        
        # Get the actual value from game state
        if field == "level":
            actual = game_state.level
        elif field == "gold":
            actual = game_state.gold
        elif field == "health":
            actual = game_state.health
        elif field == "stage":
            actual = game_state.stage
        elif field.startswith("synergy."):
            synergy_name = field.split(".")[1]
            actual = game_state.synergies.get(synergy_name, 0)
        elif field == "shop_has":
            # Special case: check if shop contains a unit
            return value in game_state.available_shops
        else:
            return False
        
        # Apply operator
        if operator == "gt":
            return actual > value
        elif operator == "gte":
            return actual >= value
        elif operator == "lt":
            return actual < value
        elif operator == "lte":
            return actual <= value
        elif operator == "eq":
            return actual == value
        elif operator == "contains":
            return value in actual
        
        return False