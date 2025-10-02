# В app/statistics.py
class StatisticsManager:
    def get_user_dashboard(self, user_id: str):
        """Дашборд статистики"""
        return {
            'win_rate': self._calculate_win_rate(user_id),
            'hands_played': self._get_hands_count(user_id),
            'best_hands': self._get_best_hands(user_id),
            'leaks': self._identify_leaks(user_id)
        }