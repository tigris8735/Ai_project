from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from app.ai_opponents import AIFactory

class GameMenus:
    """Класс для управления всеми меню и кнопками"""
    
    @staticmethod
    def get_main_menu():
        """Главное меню бота"""
        keyboard = [
            ["🎮 Быстрая игра", "⚙️ Настроить игру"],
            ["📊 Анализ руки", "📈 Моя статистика"],
            ["📚 Обучение", "👤 Мой профиль"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def get_ai_selection_menu():
        """Меню выбора AI оппонента"""
        keyboard = [
            [InlineKeyboardButton("🐟 Fish AI", callback_data="ai_fish")],
            [InlineKeyboardButton("🛡️ Nit AI", callback_data="ai_nit")],
            [InlineKeyboardButton("🎯 TAG AI", callback_data="ai_tag")],
            [InlineKeyboardButton("⚡ LAG AI", callback_data="ai_lag")],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_game_actions_menu():
        """Меню игровых действий"""
        keyboard = [
            [InlineKeyboardButton("📥 Колл", callback_data="game_call")],
            [InlineKeyboardButton("📤 Рейз", callback_data="game_raise")],
            [InlineKeyboardButton("❌ Фолд", callback_data="game_fold")],
            [InlineKeyboardButton("⚖️ Чек", callback_data="game_check")],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_ai_description(ai_type: str) -> str:
        """Получить описание AI оппонента"""
        return AIFactory.get_ai_description(ai_type)

class TextTemplates:
    """Класс для текстовых шаблонов"""
    
    @staticmethod
    def get_welcome_text(user_name: str, level: str, hands_played: int) -> str:
        return f"""
🎉 Добро пожаловать в Poker Mentor, {user_name}!

Ваш уровень: {level.title()} 🎓
Сыграно раздач: {hands_played}

📊 Доступные функции:
• 🎮 Игра против AI с разными стилями
• 📈 Анализ ваших раздач  
• 📚 Обучение стратегиям
• 📊 Отслеживание прогресса

Выберите действие из меню ниже!

💡 Для тестирования игры используйте команду /test_game
        """
    
    @staticmethod
    def get_game_start_text(ai_name: str, ai_description: str, user_cards: list, user_stack: int, pot: int) -> str:
        return (
            f"🎮 Игра началась!\n"
            f"🤖 Оппонент: {ai_name}\n"
            f"📝 {ai_description}\n\n"
            f"🃏 Ваши карты: {user_cards[0]} {user_cards[1]}\n"
            f"💰 Ваш стек: {user_stack} BB\n"
            f"🏦 Текущий банк: {pot} BB\n\n"
            f"Выберите действие:"
        )
    
    @staticmethod
    def get_help_text() -> str:
        return """
🤖 Poker Mentor - Помощь

Основные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/settings - Показать настройки
/test_game - Быстро начать тестовую игру
/choose_ai - Выбрать AI оппонента

Используйте кнопки меню для навигации.
        """