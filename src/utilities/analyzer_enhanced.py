import json
from web_scraper import DataManager

class AnalyzerEnhanced:
    """Enhanced analyzer with web-scraped data integration"""

    def __init__(self):
        # Load configuration
        with open('config.json', 'r') as f:
            self.config = json.load(f)

        # Load unit data
        with open('units.json', 'r') as f:
            self.units_data = json.load(f)

        # Initialize data manager for web-scraped data
        self.data_manager = DataManager()
        try:
            self.data_manager.load_data()
            self.has_web_data = True
        except Exception as e:
            print(f"Could not load web data: {e}")
            self.has_web_data = False

    def analyze(self, game_state):
        """Enhanced analysis with meta recommendations"""
        recommendations = []

        # 1. Rule-based recommendations
        for rule in self.config["rules"]:
            if self._evaluate_condition(rule["condition"], game_state):
                recommendations.append(rule["recommendation"])

        # 2. Meta composition recommendations (web data)
        if self.has_web_data and game_state.current_board:
            meta_recs = self._get_meta_recommendations(game_state)
            recommendations.extend(meta_recs)

        # 3. Generate final text
        if not recommendations:
            return "No specific recommendations for current state."

        result = "=== Strategic Recommendations ===\n\n"

        for i, rec in enumerate(recommendations, 1):
            result += f"{i}. {rec}\n"

        # 4. Add detailed analysis
        result += "\n=== Detailed Analysis ===\n"

        # Gold management
        result += self._analyze_gold(game_state)

        # Health status
        result += self._analyze_health(game_state)

        # Synergy analysis
        result += self._analyze_synergies(game_state)

        # Composition strength (web data)
        if self.has_web_data:
            result += self._analyze_comp_strength(game_state)

        return result

    def _get_meta_recommendations(self, game_state):
        """Get recommendations based on current meta"""
        recs = []

        # Get current units
        current_units = [u.get('unit', '') for u in game_state.current_board]

        # Get comp recommendations
        comp_recs = self.data_manager.get_comp_recommendation(current_units)

        if comp_recs:
            # Top recommendation
            top_comp = comp_recs[0]

            if top_comp['matches'] >= 2:
                missing = ', '.join(top_comp['missing'][:3])
                recs.append(
                    f"Building toward {top_comp['comp']} comp ({top_comp['tier']} tier). "
                    f"Look for: {missing}"
                )

            # Alternative if struggling
            if len(comp_recs) > 1 and game_state.health < 50:
                alt_comp = comp_recs[1]
                recs.append(
                    f"Alternative pivot: {alt_comp['comp']} (you have {alt_comp['matches']} units)"
                )

        return recs

    def _analyze_gold(self, game_state):
        """Analyze gold economy"""
        analysis = "\nGold Economy:\n"

        gold = game_state.gold

        # Interest calculation
        interest = min(gold // 10, 5)
        analysis += f"- Current gold: {gold}g (earning {interest}g interest)\n"

        # Breakpoints
        next_breakpoint = ((gold // 10) + 1) * 10
        if gold < 50:
            needed = next_breakpoint - gold
            analysis += f"- Need {needed}g for next interest breakpoint ({next_breakpoint}g)\n"

        # Leveling
        level_costs = {4: 4, 5: 8, 6: 20, 7: 36, 8: 56, 9: 80}
        if game_state.level in level_costs:
            cost = level_costs[game_state.level]
            if gold >= cost:
                analysis += f"- Can afford to level up ({cost}g)\n"
            else:
                analysis += f"- Need {cost - gold}g more to level\n"

        # Rolling
        rolls = gold // 2
        if rolls > 0:
            analysis += f"- Can roll {rolls} times (2g each)\n"

        return analysis

    def _analyze_health(self, game_state):
        """Analyze health status"""
        analysis = "\nHealth Status:\n"

        hp = game_state.health

        if hp > 80:
            analysis += "- Healthy position. Can play for late game and economy.\n"
        elif hp > 50:
            analysis += "- Decent health. Balance between economy and board strength.\n"
        elif hp > 30:
            analysis += "- Low health! Prioritize board strength over economy.\n"
        else:
            analysis += "- CRITICAL! Must stabilize immediately or risk elimination.\n"

        return analysis

    def _analyze_synergies(self, game_state):
        """Analyze active synergies"""
        analysis = "\nSynergy Analysis:\n"

        if not game_state.synergies:
            analysis += "- No active synergies detected.\n"
            return analysis

        # Check active synergies
        strong_synergies = []
        weak_synergies = []

        for synergy, count in game_state.synergies.items():
            if count >= 4:
                strong_synergies.append(f"{synergy} ({count})")
            elif count >= 2:
                weak_synergies.append(f"{synergy} ({count})")

        if strong_synergies:
            analysis += f"- Strong: {', '.join(strong_synergies)}\n"

        if weak_synergies:
            analysis += f"- Active: {', '.join(weak_synergies)}\n"

        # Recommend improvements
        if weak_synergies and game_state.level >= 6:
            analysis += "- Consider upgrading 2-trait synergies to higher breakpoints\n"

        return analysis

    def _analyze_comp_strength(self, game_state):
        """Analyze composition strength using web data"""
        analysis = "\nComposition Strength:\n"

        current_units = [u.get('unit', '') for u in game_state.current_board]

        if not current_units:
            return analysis

        # Get meta comp matches
        comp_recs = self.data_manager.get_comp_recommendation(current_units)

        if comp_recs:
            top_match = comp_recs[0]
            completion = (top_match['matches'] / len(top_match['comp'].split())) * 100

            analysis += f"- Closest meta comp: {top_match['comp']} ({completion:.0f}% complete)\n"
            analysis += f"- Tier: {top_match['tier']}\n"

            if top_match['missing']:
                analysis += f"- Missing key units: {', '.join(top_match['missing'][:5])}\n"

        # Check champion costs
        total_cost = 0
        for unit in game_state.current_board:
            unit_name = unit.get('unit', '')
            champ_data = self.data_manager.get_champion_info(unit_name)
            if champ_data:
                total_cost += champ_data.get('cost', 1)

        avg_cost = total_cost / len(current_units) if current_units else 0
        analysis += f"- Average unit cost: {avg_cost:.1f}\n"

        return analysis

    def _evaluate_condition(self, condition, game_state):
        """Evaluate a single condition against game state"""
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]

        # Get actual value from game state
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

    def update_web_data(self):
        """Force update web-scraped data"""
        try:
            self.data_manager.scraper.update_all_data()
            self.data_manager.load_data()
            self.has_web_data = True
            return "Data updated successfully"
        except Exception as e:
            return f"Update failed: {e}"
