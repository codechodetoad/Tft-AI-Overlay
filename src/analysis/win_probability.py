class WinProbabilityCalculator:
    """Calculate win probability based on game state"""

    def calculate(self, game_state):
        """
        Calculate probabilities for different placements

        Returns:
            dict with top1, top4, bottom4 probabilities
        """
        # Extract features
        health = game_state.get('health', 100)
        level = game_state.get('level', 1)
        gold = game_state.get('gold', 0)
        board = game_state.get('current_board', [])
        stage = game_state.get('stage', '1-1')

        # Calculate board strength
        board_strength = self._calc_board_strength(board)

        # Calculate economy score
        economy_score = min(gold / 50, 1.0)

        # Stage factor (later stages reduce variance)
        stage_num = self._parse_stage(stage)
        stage_factor = min(stage_num / 7, 1.0)

        # Combine features into score
        health_score = health / 100
        level_score = level / 9
        board_score = min(board_strength / 100, 1.0)

        # Weighted combination
        base_score = (
            health_score * 0.35 +
            board_score * 0.40 +
            level_score * 0.15 +
            economy_score * 0.10
        )

        # Apply stage factor (more certainty late game)
        adjusted_score = base_score * (0.7 + 0.3 * stage_factor)

        # Convert to placement probabilities
        top1_prob = max(0, min(1, adjusted_score ** 2))
        top4_prob = max(0, min(1, adjusted_score * 1.5))
        bottom4_prob = max(0, 1 - top4_prob)

        return {
            'top1': round(top1_prob * 100, 1),
            'top4': round(top4_prob * 100, 1),
            'bottom4': round(bottom4_prob * 100, 1),
            'score': round(adjusted_score * 100, 1)
        }

    def _calc_board_strength(self, board):
        """Calculate board strength score"""
        if not board:
            return 0

        total_strength = 0

        for unit in board:
            cost = unit.get('cost', 1)
            stars = unit.get('stars', 1)
            items = len(unit.get('items', []))

            # Cost matters most, stars exponentially, items linearly
            unit_strength = cost * 10 + (stars ** 2) * 5 + items * 3

            total_strength += unit_strength

        return total_strength

    def _parse_stage(self, stage_str):
        """Parse stage string like '3-2' into numeric value"""
        try:
            parts = stage_str.split('-')
            return int(parts[0])
        except:
            return 1
