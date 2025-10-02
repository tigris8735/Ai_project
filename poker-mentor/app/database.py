import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, GameSession, HandHistory, UserStats
from app.config import config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.database_url = config.get('DATABASE_URL', 'sqlite:///poker_mentor.db')
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def init_db(self):
        """Инициализация базы данных - создание таблиц"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("База данных инициализирована")
            print("✅ База данных создана успешно")
        except Exception as e:
            logger.error(f"Ошибка инициализации БД: {e}")
            raise
    
    def get_session(self):
        """Получить сессию БД"""
        return self.SessionLocal()
    
    def add_user(self, telegram_id, username=None, first_name=None, last_name=None):
        """Добавить нового пользователя"""
        session = self.get_session()
        try:
            # Проверяем, существует ли пользователь
            existing_user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if existing_user:
                return existing_user
            
            # Создаем нового пользователя
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            
            # Создаем статистику для пользователя
            user_stats = UserStats(user_id=new_user.id)
            session.add(user_stats)
            session.commit()
            
            logger.info(f"Создан новый пользователь: {new_user}")
            return new_user
            
        except Exception as e:
            session.rollback()
            logger.error(f"Ошибка создания пользователя: {e}")
            raise
        finally:
            session.close()
    
    def get_user(self, telegram_id):
        """Получить пользователя по telegram_id"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            return user
        except Exception as e:
            logger.error(f"Ошибка получения пользователя: {e}")
            return None
        finally:
            session.close()
    
    def update_user_activity(self, telegram_id):
        """Обновить время последней активности"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            if user:
                user.last_active = datetime.utcnow()
                session.commit()
        except Exception as e:
            logger.error(f"Ошибка обновления активности: {e}")
            session.rollback()
        finally:
            session.close()

# Глобальный объект базы данных
db = Database()