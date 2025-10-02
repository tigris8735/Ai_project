import logging
from datetime import datetime, timedelta
from app.database import db
from app.config import config

logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self):
        self.db = db
    
    def get_user_sessions(self, telegram_id: int, days: int = 30, limit: int = 20):
        """Получить сессии пользователя"""
        try:
            session = self.db.get_session()
            user = session.query(db.User).filter(db.User.telegram_id == telegram_id).first()
            
            if not user:
                return []
            
            # Здесь будет запрос к GameSession
            # Пока заглушка
            return [
                {
                    'id': 1,
                    'date': '2024-01-15',
                    'ai_opponent': 'Fish AI',
                    'hands_played': 15,
                    'result': '+25 BB',
                    'duration': '15 мин'
                }
            ]
            
        except Exception as e:
            logger.error(f"Ошибка получения истории: {e}")
            return []
        finally:
            session.close()
    
    def get_session_details(self, session_id: int):
        """Детали сессии"""
        return {
            'session_info': {
                'id': session_id,
                'date': '2024-01-15 14:30',
                'duration': '15 минут',
                'ai_opponent': 'Fish AI',
                'stake': '1/2'
            },
            'hands': [
                {'hand_id': 1, 'result': 'Win +15BB', 'cards': 'A♠ K♥'},
                {'hand_id': 2, 'result': 'Loss -2BB', 'cards': '7♦ 2♣'},
            ],
            'statistics': {
                'total_hands': 15,
                'win_rate': '60%',
                'avg_profit': '+1.7 BB/hand',
                'best_hand': 'A♠ A♥ (Win +45BB)'
            }
        }

# Глобальный экземпляр
history_manager = HistoryManager()