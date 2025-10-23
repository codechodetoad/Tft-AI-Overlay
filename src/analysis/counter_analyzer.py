class CounterAnalyzer:
    def analyze_threats(self, enemy_comps):
        threats = []
        for enemy in enemy_comps:
            threat_level = sum(u.get('cost', 1) * u.get('stars', 1) for u in enemy.get('board', [])) / 10
            threats.append({'threat': threat_level, 'counters': self._get_counters(enemy)})
        return threats
    
    def _get_counters(self, comp):
        return ['Build tank items', 'Stack MR', 'Position defensively']
