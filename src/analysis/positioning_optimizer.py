class PositioningOptimizer:
    """Optimize champion positioning on the hex board"""

    def __init__(self, db_manager=None):
        self.db = db_manager

        # Standard positioning templates
        self.front_line = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 5)]
        self.back_line = [(3, 0), (3, 6), (2, 1), (2, 5), (3, 3)]
        self.mid_line = [(1, 2), (1, 4), (2, 2), (2, 4), (2, 3)]

    def optimize(self, board):
        """
        Optimize positioning for given board

        Args:
            board: List of units with name, cost, items, traits

        Returns:
            dict with positioning recommendations
        """
        if not board:
            return {'positioning': {}, 'recommendations': []}

        # Categorize units
        tanks = []
        carries = []
        supports = []

        for unit in board:
            if self._is_carry(unit):
                carries.append(unit)
            elif self._is_tank(unit):
                tanks.append(unit)
            else:
                supports.append(unit)

        # Generate positioning
        positioning = {}
        recommendations = []

        # Place tanks front
        for i, tank in enumerate(tanks):
            if i < len(self.front_line):
                pos = self.front_line[i]
                positioning[tank['unit']] = pos
                recommendations.append({
                    'unit': tank['unit'],
                    'position': pos,
                    'reason': 'Frontline tank to absorb damage'
                })

        # Place carries in back corners (protected)
        for i, carry in enumerate(carries):
            if i < len(self.back_line):
                pos = self.back_line[i]
                positioning[carry['unit']] = pos
                recommendations.append({
                    'unit': carry['unit'],
                    'position': pos,
                    'reason': 'Backline carry for maximum damage output'
                })

        # Place supports in mid
        for i, support in enumerate(supports):
            if i < len(self.mid_line):
                pos = self.mid_line[i]
                positioning[support['unit']] = pos
                recommendations.append({
                    'unit': support['unit'],
                    'position': pos,
                    'reason': 'Midline support for utility'
                })

        return {
            'positioning': positioning,
            'recommendations': recommendations,
            'summary': f"{len(tanks)} tanks front, {len(carries)} carries back, {len(supports)} supports mid"
        }

    def _is_carry(self, unit):
        """Check if unit is a carry"""
        # Carries have damage items or are high cost
        carry_items = ['Infinity Edge', 'Deathblade', 'Giant Slayer', 'Guinsoo', 
                       'Rabadon', 'Jeweled Gauntlet', 'Last Whisper']

        items = unit.get('items', [])
        has_carry_item = any(item in carry_items for item in items)

        cost = unit.get('cost', 1)
        is_high_cost = cost >= 4

        return has_carry_item or is_high_cost

    def _is_tank(self, unit):
        """Check if unit is a tank"""
        tank_items = ['Bramble Vest', 'Dragon Claw', 'Gargoyle Stoneplate',
                      'Warmog', 'Sunfire Cape', 'Titan\'s Resolve']

        items = unit.get('items', [])
        has_tank_item = any(item in tank_items for item in items)

        traits = unit.get('traits', [])
        tank_traits = ['Bruiser', 'Vanguard', 'Bodyguard', 'Colossus']
        has_tank_trait = any(trait in tank_traits for trait in traits)

        return has_tank_item or has_tank_trait

    def counter_position(self, enemy_comp_type):
        """Suggest positioning adjustments vs specific comps"""
        counter_advice = {
            'Assassins': 'Clump in corner to protect carries from assassin jumps',
            'AoE': 'Spread units to minimize AoE damage',
            'Shroud': 'Position carries on opposite side from enemy carries',
            'Frontline': 'Stack one side to focus fire'
        }

        return counter_advice.get(enemy_comp_type, 'Standard positioning')
