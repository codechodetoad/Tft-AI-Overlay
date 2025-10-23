import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.database.db_manager import DatabaseManager
from src.scrapers.orchestrator import ScrapingOrchestrator
from src.analysis.win_probability import WinProbabilityCalculator
from src.analysis.positioning_optimizer import PositioningOptimizer
from src.analysis.itemization_guide import ItemizationGuide
from src.analysis.counter_analyzer import CounterAnalyzer
from src.automation.game_detector import GameDetector

class MasterController:
    """Central controller orchestrating all systems"""
    
    def __init__(self):
        print("Initializing TFT Overlay Master Controller...")
        
        # Core systems
        self.db = DatabaseManager()
        self.scraper = ScrapingOrchestrator(self.db)
        
        # Analysis systems
        self.win_calc = WinProbabilityCalculator()
        self.positioning = PositioningOptimizer(self.db)
        self.itemization = ItemizationGuide(self.db)
        self.counter_analyzer = CounterAnalyzer()
        self.game_detector = GameDetector()
        
        print("Master Controller initialized!")
    
    def initialize_data(self, force_update=False):
        """Initialize/update all game data"""
        print("Updating game data...")
        self.scraper.update_all_data(force=force_update)
    
    def analyze_game_state(self, game_state):
        """
        Comprehensive analysis of game state
        
        Args:
            game_state: dict with level, gold, health, stage, current_board, etc
            
        Returns:
            dict with all analysis results
        """
        analysis = {}
        
        # Win probability
        try:
            analysis['win_probability'] = self.win_calc.calculate(game_state)
        except Exception as e:
            analysis['win_probability'] = {'error': str(e)}
        
        # Positioning
        try:
            board = game_state.get('current_board', [])
            analysis['positioning'] = self.positioning.optimize(board)
        except Exception as e:
            analysis['positioning'] = {'error': str(e)}
        
        # Itemization
        try:
            components = game_state.get('components', [])
            board = game_state.get('current_board', [])
            analysis['itemization'] = self.itemization.recommend_items(components, board)
        except Exception as e:
            analysis['itemization'] = {'error': str(e)}
        
        # Economy advice
        analysis['economy'] = self._get_economy_advice(game_state)
        
        return analysis
    
    def _get_economy_advice(self, state):
        """Generate economy advice"""
        gold = state.get('gold', 0)
        level = state.get('level', 1)
        
        advice = []
        
        # Interest
        if gold < 50:
            next_breakpoint = ((gold // 10) + 1) * 10
            needed = next_breakpoint - gold
            advice.append(f"Save {needed}g for next interest breakpoint")
        
        # Leveling
        level_costs = {4: 4, 5: 8, 6: 20, 7: 36, 8: 56, 9: 80}
        if level in level_costs:
            cost = level_costs[level]
            if gold >= cost:
                advice.append(f"Can afford to level ({cost}g)")
        
        # Rolling
        rolls = gold // 2
        if rolls > 0:
            advice.append(f"Can roll {rolls} times")
        
        return advice
    
    def get_comp_recommendations(self, current_units):
        """Get composition recommendations from database"""
        try:
            top_comps = self.db.get_top_comps(limit=5)
            
            recommendations = []
            for comp in top_comps:
                matches = len(set(current_units) & set(comp['champions']))
                if matches > 0:
                    recommendations.append({
                        'name': comp['name'],
                        'matches': matches,
                        'tier': comp['tier'],
                        'win_rate': comp['win_rate']
                    })
            
            return sorted(recommendations, key=lambda x: x['matches'], reverse=True)
        except:
            return []
    
    def start_auto_monitoring(self):
        """Start automatic game detection and monitoring"""
        self.game_detector.start_monitoring(lambda: print("Game detected!"))
        print("Auto-monitoring started")
