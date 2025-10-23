class ItemizationGuide:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def recommend_items(self, components, board):
        recommendations = []
        
        for unit in board:
            if len(unit.get('items', [])) >= 3:
                continue
            
            suggested_items = self._get_best_items_for_unit(unit, components)
            if suggested_items:
                recommendations.append({
                    'unit': unit['unit'],
                    'items': suggested_items[:2]
                })
        
        return recommendations
    
    def _get_best_items_for_unit(self, unit, available_components):
        cost = unit.get('cost', 1)
        
        if cost >= 4:
            return ['Infinity Edge', 'Giant Slayer', 'Deathblade']
        elif cost >= 2:
            return ['Blue Buff', 'Rabadon', 'Morello']
        else:
            return ['Sunfire Cape', 'Warmog', 'Bramble Vest']
