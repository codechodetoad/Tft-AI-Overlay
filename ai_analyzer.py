import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAnalyzer:
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            self.use_ai = False
            print("Warning: OpenAI API key not set. Using rule-based analysis only.")
        else:
            self.use_ai = True
            self.client = OpenAI(api_key=api_key)
            self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

        # Load configuration
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        # Load unit data
        with open('units.json', 'r') as f:
            self.units_data = json.load(f)

    def analyze(self, game_state):
        """Analyze game state and return recommendation"""
        # First, get rule-based recommendations
        rule_based_recommendations = self._get_rule_based_recommendations(game_state)

        # If AI is enabled, enhance with AI analysis
        if self.use_ai:
            try:
                ai_recommendations = self._get_ai_recommendations(game_state, rule_based_recommendations)
                return ai_recommendations
            except Exception as e:
                print(f"AI Analysis error: {e}")
                return rule_based_recommendations
        else:
            return rule_based_recommendations

    def _get_rule_based_recommendations(self, game_state):
        """Get recommendations based on predefined rules"""
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

    def _get_ai_recommendations(self, game_state, rule_based_recs):
        """Get AI-enhanced recommendations using OpenAI"""
        # Prepare game state for AI
        game_state_summary = {
            "stage": game_state.stage,
            "level": game_state.level,
            "gold": game_state.gold,
            "health": game_state.health,
            "current_board": [f"{u['unit']} ({u['stars']}★)" for u in game_state.current_board],
            "synergies": game_state.synergies,
            "bench": game_state.bench,
            "shop": game_state.available_shops
        }

        # Create prompt for AI
        prompt = f"""You are an expert TFT (Teamfight Tactics) coach analyzing a game state.

Current Game State:
{json.dumps(game_state_summary, indent=2)}

Rule-based recommendations:
{rule_based_recs}

Based on this game state, provide strategic advice covering:
1. Immediate actions (level up, roll, or save gold)
2. Board positioning improvements
3. Which units to look for in shop
4. Synergy building recommendations
5. Win condition strategy

Keep the response concise and actionable (3-5 key recommendations).
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional TFT coach providing strategic advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content

            # Combine rule-based and AI recommendations
            result = "=== AI-Enhanced Analysis ===\n\n"
            result += ai_response
            result += "\n\n=== Rule-Based Analysis ===\n\n"
            result += rule_based_recs

            return result

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

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

    def analyze_comp_strength(self, game_state):
        """
        Analyze the strength of current composition
        Returns a score from 0-100
        """
        score = 50  # Base score

        # Add points for synergies
        for synergy, count in game_state.synergies.items():
            if count >= 3:
                score += 10
            elif count >= 2:
                score += 5

        # Add points for starred units
        for unit in game_state.current_board:
            stars = unit.get('stars', 1)
            if stars >= 3:
                score += 10
            elif stars >= 2:
                score += 5

        # Adjust based on board size
        board_size = len(game_state.current_board)
        if board_size >= game_state.level:
            score += 10
        elif board_size < game_state.level - 2:
            score -= 10

        # Cap score at 100
        return min(100, score)
