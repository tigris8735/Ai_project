import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.config import config
# from app.database import db  # Пока закомментируем БД

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class PokerMentorBot:
    def __init__(self):
        # Проверяем конфигурацию
        is_valid, message = config.validate()
        if not is_valid:
            logger.error(f"Конфигурация невалидна: {message}")
            raise ValueError(message)
        
        # Инициализируем базу данных (пока закомментировано)
        # db.init_db()
        
        self.token = config.get('TELEGRAM_BOT_TOKEN')
        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()  # ← ИСПРАВЛЕНО: добавил точку перед setup_handlers
        logger.info("Poker Mentor Bot инициализирован")
    
    def _setup_handlers(self):  # ← ИСПРАВЛЕНО: правильное название метода
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.show_help))
        self.application.add_handler(CommandHandler("settings", self.settings))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        # Пока без БД
        # db_user = db.add_user(
        #     telegram_id=user.id,
        #     username=user.username,
        #     first_name=user.first_name,
        #     last_name=user.last_name
        # )
        
        welcome_text = f"""
🎉 Добро пожаловать в Poker Mentor, {user.first_name}!

📊 Доступные функции:
• 🎮 Игра против AI с разными стилями
• 📈 Анализ ваших раздач  
• 📚 Обучение стратегиям
• 📊 Отслеживание прогресса

Выберите действие из меню ниже!
        """
        
        keyboard = [
            ["🎮 Быстрая игра", "⚙️ Настроить игру"],
            ["📊 Анализ руки", "📈 Моя статистика"],
            ["📚 Обучение", "👤 Мой профиль"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"New user started: {user.id} - {user.username}")
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
🤖 Poker Mentor - Помощь

Основные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/settings - Показать настройки

Используйте кнопки меню для навигации:
• 🎮 Быстрая игра - начать игру с настройками по умолчанию
• ⚙️ Настроить игру - выбрать параметры тренировки
• 📊 Анализ руки - разобрать конкретную раздачу
• 📈 Моя статистика - посмотреть прогресс обучения
• 📚 Обучение - изучить теорию покера
• 👤 Мой профиль - настроить аккаунт
        """
        await update.message.reply_text(help_text)
    
    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать настройки"""
        await update.message.reply_text(
            "⚙️ Текущие настройки:\n"
            f"• Версия: 1.0\n"
            f"• База данных: {config.get('DATABASE_URL', 'Не настроена')}\n"
            f"• Ставки: {config.get('DEFAULT_STAKE', '1/2')}\n\n"
            "Для изменения настроек отредактируйте файл config.txt"
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        text = update.message.text
        user = update.effective_user
        
        if text == "🎮 Быстрая игра":
            await self.quick_game(update, context)
        elif text == "📊 Анализ руки":
            await self.analyze_hand(update, context)
        elif text == "📈 Моя статистика":
            await self.show_stats(update, context)
        elif text == "👤 Мой профиль":
            await self.show_profile(update, context)
        elif text == "📚 Обучение":
            await self.show_learning(update, context)
        elif text == "⚙️ Настроить игру":
            await self.setup_game(update, context)
        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки меню или команды!")
    
    async def quick_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Быстрый старт игры"""
        await update.message.reply_text(
            "🎮 Запускаем быструю игру!\n\n"
            "Параметры по умолчанию:\n"
            "• Тип: Cash Game\n"
            "• Блайнды: 1/2\n" 
            "• Оппонент: Сбалансированный AI\n\n"
            "⚡ Игра начинается..."
        )
        # Здесь будет логика начала игры
    
    async def analyze_hand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Анализ руки"""
        await update.message.reply_text(
            "📊 Анализ раздачи\n\n"
            "Пожалуйста, опишите раздачу в формате:\n\n"
            "Позиция: [ваша позиция]\n"
            "Карты: [ваши карты]\n" 
            "Действия: [ход раздачи]\n\n"
            "Или используйте специальный формат ввода."
        )
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику"""
        await update.message.reply_text(
            "📈 Ваша статистика\n\n"
            "📊 Общая:\n"
            "• Сыграно раздач: 0\n"
            "• Winrate: 0%\n"
            "• Лучшая рука: -\n\n"
            "🎯 В разработке...\n"
            "Сбор статистики начнется после первых игр!"
        )
    
    async def show_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать профиль"""
        user = update.effective_user
        await update.message.reply_text(
            f"👤 Ваш профиль\n\n"
            f"ID: {user.id}\n"
            f"Имя: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'не установлен'}\n"
            f"Уровень: Новичок 🎓\n\n"
            f"Настройки профиля появятся позже!"
        )
    
    async def show_learning(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать обучение"""
        await update.message.reply_text(
            "📚 Обучение покеру\n\n"
            "Доступные разделы:\n"
            "• 📖 Основы покера\n"
            "• 🎯 Префлоп стратегии\n" 
            "• 📊 Математика покера\n"
            "• 🃏 Позиционная игра\n\n"
            "Выберите тему для изучения!"
        )
    
    async def setup_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Настройка игры"""
        await update.message.reply_text(
            "⚙️ Настройка игры\n\n"
            "Доступные параметры:\n"
            "• Тип игры: Cash/Tournament\n"
            "• Размер стека\n"
            "• Стиль оппонента\n"
            "• Уровень сложности\n\n"
            "Эта функция в разработке!"
        )
    
    def run(self):
        """Запуск бота"""
        logger.info("Starting Poker Mentor Bot...")
        print("🤖 Запуск Poker Mentor Bot...")
        print("🛑 Для остановки нажмите Ctrl+C")
        self.application.run_polling()

# Точка входа
if __name__ == "__main__":
    try:
        bot = PokerMentorBot()
        bot.run()
    except ValueError as e:
        print(f"❌ Ошибка запуска: {e}")
        print("\n🔧 Инструкция по настройке:")
        print("1. Откройте файл config.txt")
        print("2. Замените 'your_bot_token_here' на ваш токен от @BotFather")
        print("3. Сохраните файл и запустите бота снова")
    except Exception as e:
        print(f"💥 Неожиданная ошибка: {e}")