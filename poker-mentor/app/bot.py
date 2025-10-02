import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from app.config import config
from app.database import db
from app.game_menus import GameMenus, TextTemplates
from app.game_manager import GameManager

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class PokerMentorBot:
    """Главный класс бота - конструктор функциональности"""
    
    def __init__(self):
        # Проверяем конфигурацию
        is_valid, message = config.validate()
        if not is_valid:
            logger.error(f"Конфигурация невалидна: {message}")
            raise ValueError(message)
        
        # Инициализируем базу данных
        db.init_db()
        
        # Инициализируем менеджер игр
        self.game_manager = GameManager()
        
        # Создаем приложение Telegram
        self.token = config.get('TELEGRAM_BOT_TOKEN')
        self.application = Application.builder().token(self.token).build()
        
        # Настраиваем обработчики
        self._setup_handlers()
        logger.info("Poker Mentor Bot инициализирован")
    
    def _setup_handlers(self):
        """Настройка обработчиков команд - конструктор функциональности"""
        # Команды
        self.application.add_handler(CommandHandler("start", self._handle_start))
        self.application.add_handler(CommandHandler("help", self._handle_help))
        self.application.add_handler(CommandHandler("settings", self._handle_settings))
        self.application.add_handler(CommandHandler("test_game", self._handle_test_game))
        self.application.add_handler(CommandHandler("choose_ai", self._handle_choose_ai))
        
        # Обработчики кнопок и сообщений
        self.application.add_handler(CallbackQueryHandler(self._handle_callback_query))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text_message))
    
    # ===== ОСНОВНЫЕ ОБРАБОТЧИКИ =====
    
    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        # Сохраняем пользователя в БД
        db_user = db.add_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Получаем статистику
        user_stats = db.get_user_stats(db_user['id'])
        hands_played = user_stats['total_hands_played'] if user_stats else 0
        
        # Отправляем приветствие
        welcome_text = TextTemplates.get_welcome_text(
            user.first_name, db_user['level'], hands_played
        )
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=GameMenus.get_main_menu()
        )
    
    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        await update.message.reply_text(TextTemplates.get_help_text())
    
    async def _handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /settings"""
        await update.message.reply_text(
            "⚙️ Текущие настройки:\n"
            f"• Версия: 1.0\n"
            f"• База данных: {config.get('DATABASE_URL', 'Не настроена')}\n"
            f"• Ставки: {config.get('DEFAULT_STAKE', '1/2')}\n\n"
            "Для изменения настроек отредактируйте файл config.txt"
        )
    
    async def _handle_test_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /test_game"""
        user_id = str(update.effective_user.id)
        
        # Создаем тестовую игру
        game = self.game_manager.create_game(user_id, "fish")
        game_state = self.game_manager.get_game_state(user_id)
        
        # Отправляем информацию о игре
        game_text = TextTemplates.get_game_start_text(
            "Fish", 
            GameMenus.get_ai_description("fish"),
            game_state["user_cards"],
            game_state["user_stack"],
            game_state["pot"]
        )
        
        await update.message.reply_text(game_text)
        await self._show_game_actions(update, context, user_id)
    
    async def _handle_choose_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /choose_ai"""
        await update.message.reply_text(
            "🤖 Выберите тип AI оппонента:",
            reply_markup=GameMenus.get_ai_selection_menu()
        )
    
    # ===== ОБРАБОТЧИКИ КНОПОК =====
    
    async def _handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        callback_data = query.data
        
        # Обрабатываем выбор AI
        if callback_data.startswith("ai_"):
            ai_type = callback_data[3:]
            await self._start_game_with_ai(query, user_id, ai_type)
        
        # Обрабатываем игровые действия
        elif callback_data.startswith("game_"):
            action = callback_data[5:]  # Убираем "game_"
            await self._handle_game_action(query, user_id, action)
    
    async def _handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        text = update.message.text
        user = update.effective_user
        
        # Обрабатываем кнопки главного меню
        if text == "🎮 Быстрая игра":
            await self._handle_test_game(update, context)
        elif text == "📊 Анализ руки":
            await update.message.reply_text("📊 Анализ руки - в разработке")
        elif text == "📈 Моя статистика":
            await update.message.reply_text("📈 Статистика - в разработке")
        elif text == "👤 Мой профиль":
            await update.message.reply_text("👤 Профиль - в разработке")
        elif text == "📚 Обучение":
            await update.message.reply_text("📚 Обучение - в разработке")
        elif text == "⚙️ Настроить игру":
            await update.message.reply_text("⚙️ Настройка игры - в разработке")
        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки меню или команды!")
    
    # ===== ИГРОВАЯ ЛОГИКА =====
    
    async def _start_game_with_ai(self, query, user_id: str, ai_type: str):
        """Начать игру с выбранным AI"""
        try:
            # Создаем игру
            game = self.game_manager.create_game(user_id, ai_type)
            game_state = self.game_manager.get_game_state(user_id)
            
            # Отправляем информацию о игре
            game_text = TextTemplates.get_game_start_text(
                game_state["ai_name"],
                GameMenus.get_ai_description(ai_type),
                game_state["user_cards"],
                game_state["user_stack"],
                game_state["pot"]
            )
            
            await query.edit_message_text(game_text)
            await self._show_game_actions_by_chat(
                query, query.message.chat_id, user_id
            )
            
        except Exception as e:
            await query.edit_message_text(f"Ошибка начала игры: {e}")
    
    async def _handle_game_action(self, query, user_id: str, action: str):
        """Обработать игровое действие"""
        # Обрабатываем действие через менеджер игр
        result = self.game_manager.process_player_action(user_id, action)
        
        if "error" in result:
            await query.edit_message_text(result["error"])
            return
        
        # Формируем ответ
        response_text = result["message"]
        if "ai_message" in result:
            response_text += f"\n{result['ai_message']}"
        
        response_text += f"\n\n💰 Банк: {result['pot']} BB"
        response_text += f"\n💵 Ваш стек: {result['player_stack']} BB"
        
        # Добавляем информацию о community cards
        if result.get("community_cards"):
            street = "Флоп" if len(result["community_cards"]) == 3 else "Терн" if len(result["community_cards"]) == 4 else "Ривер"
            response_text += f"\n\n🃏 {street}: {' '.join(str(card) for card in result['community_cards'])}"
        
        # Обрабатываем завершение игры
        if not result.get("game_continues", True):
            if "winner" in result:
                response_text += f"\n\n🏆 Победитель: {result['winner']}"
                response_text += f"\n🎯 Комбинация: {result['winning_hand']}"
            self.game_manager.end_game(user_id)
            await query.edit_message_text(response_text)
            return
        
        # Продолжаем игру
        await query.edit_message_text(response_text)
        await self._show_game_actions_by_chat(query, query.message.chat_id, user_id)
    
    # ===== УТИЛИТЫ ДЛЯ ОТОБРАЖЕНИЯ =====
    
    async def _show_game_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
        """Показать игровые действия"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите действие:",
            reply_markup=GameMenus.get_game_actions_menu()
        )
    
    async def _show_game_actions_by_chat(self, update, chat_id: int, user_id: str):
        """Показать игровые действия по chat_id"""
        await update._bot.send_message(
            chat_id=chat_id,
            text="Выберите действие:",
            reply_markup=GameMenus.get_game_actions_menu()
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