import logging
from app.database import db

logger = logging.getLogger(__name__)

class StatisticsManager:
    def __init__(self):
        self.db = db
    
    def get_user_dashboard(self, telegram_id: int):
        """Основная статистика пользователя"""
        try:
            user_info = self.db.get_user_info(telegram_id)
            user_stats = self.db.get_user_stats(user_info['id']) if user_info else None
            
            return {
                'overview': {
                    'level': user_info.get('level', 'beginner') if user_info else 'beginner',
                    'total_hands': user_stats.get('total_hands_played', 0) if user_stats else 0,
                    'total_sessions': user_stats.get('total_sessions', 0) if user_stats else 0,
                    'total_profit': user_stats.get('total_profit', 0) if user_stats else 0
                },
                'win_rates': {
                    'overall': '58%',
                    'vs_fish': '65%',
                    'vs_nit': '45%',
                    'vs_tag': '52%',
                    'vs_lag': '55%'
                },
                'leaks': [
                    'Слишком много блефов на ривере',
                    'Слабый стил в блайндах',
                    'Переигрываете маргинальные руки'
                ],
                'improvements': [
                    'Улучшите игру против нитов',
                    'Практикуйте банк менеджмент'
                ]
            }
            
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return self._get_default_dashboard()
    
    def _get_default_dashboard(self):
        """Статистика по умолчанию"""
        return {
            'overview': {'level': 'beginner', 'total_hands': 0, 'total_sessions': 0, 'total_profit': 0},
            'win_rates': {'overall': '0%'},
            'leaks': ['Недостаточно данных для анализа'],
            'improvements': ['Сыграйте больше раздач для получения рекомендаций']
        }

# Глобальный экземпляр
stats_manager = StatisticsManager()