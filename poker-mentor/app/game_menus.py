from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from app.ai_opponents import AIFactory
from typing import Dict, List, Any, Optional  # или другие типы, которые вы используете

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
    
    @staticmethod
    def get_hand_analysis_text(analysis: Dict) -> str:
        """Текст анализа руки"""
        return f"""
📊 **Анализ руки: {analysis['hand']}**

💪 **Сила:** {analysis['strength']:.2f}
🏷️ **Категория:** {analysis['category']}
🎪 **Позиция:** {analysis['position']}

📋 **Рекомендации:**
{chr(10).join('• ' + rec for rec in analysis['recommendations'])}
        """
    
    @staticmethod
    def get_postflop_analysis_text(analysis: Dict) -> str:
        """Текст анализа постфлопа"""
        return f"""
🎯 **Анализ постфлопа**

📈 **Эквити:** {analysis['equity']:.1%}
💪 **Сила руки:** {analysis['hand_strength']:.2f}

💡 **Рекомендации:**
{chr(10).join('• ' + rec for rec in analysis['recommendations'])}
        """
    
    @staticmethod
    def get_hand_history_analysis_text(analysis: Dict) -> str:
        """Текст анализа истории раздачи"""
        rating_emoji = "⭐" * analysis['rating']
        
        text = f"""
📈 **Анализ раздачи**

🏆 **Рейтинг:** {analysis['rating']}/10 {rating_emoji}

"""
        
        if analysis['mistakes']:
            text += f"❌ **Ошибки:**\n{chr(10).join('• ' + mistake for mistake in analysis['mistakes'])}\n\n"
        
        if analysis['good_plays']:
            text += f"✅ **Хорошие решения:**\n{chr(10).join('• ' + play for play in analysis['good_plays'])}\n\n"
        
        if analysis['improvement_tips']:
            text += f"💡 **Советы по улучшению:**\n{chr(10).join('• ' + tip for tip in analysis['improvement_tips'])}"
        
        return text

# Добавляем новые меню
class AnalysisMenus:
    """Меню для анализа"""
    
    @staticmethod
    def get_analysis_menu():
        """Меню анализа"""
        keyboard = [
            [InlineKeyboardButton("🃏 Анализ префлоп руки", callback_data="analyze_preflop")],
            [InlineKeyboardButton("📊 Анализ постфлопа", callback_data="analyze_postflop")],
            [InlineKeyboardButton("📈 Анализ раздачи", callback_data="analyze_hand_history")],
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_position_selection_menu():
        """Меню выбора позиции"""
        keyboard = [
            [InlineKeyboardButton("🎪 Ранняя позиция", callback_data="position_early")],
            [InlineKeyboardButton("🎪 Средняя позиция", callback_data="position_middle")],
            [InlineKeyboardButton("🎪 Поздняя позиция", callback_data="position_late")],
            [InlineKeyboardButton("🎪 Блайнды", callback_data="position_blinds")],
        ]
        return InlineKeyboardMarkup(keyboard) 
class AnalysisMenus:
    @staticmethod
    async def show_analysis_options(update, context):
        # Ваша логика для меню анализа
        keyboard = [
            ["Анализ руки", "История игр"],
            ["Статистика", "Назад"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Выберите тип анализа:",
            reply_markup=reply_markup
        )
    
    @staticmethod
    async def handle_hand_analysis(update, context):
        # Логика анализа конкретной руки
        pass
    
    @staticmethod
    async def handle_game_history(update, context):
        # Логика показа истории игр
        pass