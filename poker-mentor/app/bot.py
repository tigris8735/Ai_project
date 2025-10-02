import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from app.config import config
from app.database import db
from app.poker_engine import PokerGame, Action

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
        
        # Инициализируем базу данных
        db.init_db()
        
        self.token = config.get('TELEGRAM_BOT_TOKEN')
        self.application = Application.builder().token(self.token).build()
        self.active_games = {}  # Хранилище активных игр
        self._setup_handlers()
        logger.info("Poker Mentor Bot инициализирован")
    
    def _setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.show_help))
        self.application.add_handler(CommandHandler("settings", self.settings))
        self.application.add_handler(CommandHandler("test_game", self.test_game))
        self.application.add_handler(CallbackQueryHandler(self.handle_button_click))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        # Сохраняем/обновляем пользователя в БД
        db_user = db.add_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Получаем статистику пользователя
        user_stats = db.get_user_stats(db_user['id'])
        hands_played = user_stats['total_hands_played'] if user_stats else 0
        
        welcome_text = f"""
🎉 Добро пожаловать в Poker Mentor, {user.first_name}!

Ваш уровень: {db_user['level'].title()} 🎓
Сыграно раздач: {hands_played}

📊 Доступные функции:
• 🎮 Игра против AI с разными стилями
• 📈 Анализ ваших раздач  
• 📚 Обучение стратегиям
• 📊 Отслеживание прогресса

Выберите действие из меню ниже!

💡 Для тестирования игры используйте команду /test_game
        """
        
        keyboard = [
            ["🎮 Быстрая игра", "⚙️ Настроить игру"],
            ["📊 Анализ руки", "📈 Моя статистика"],
            ["📚 Обучение", "👤 Мой профиль"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"New user started: {user.id} - {user.username}")
    
    async def test_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Тестовая команда для быстрого запуска игры"""
        user = update.effective_user
        user_id = str(user.id)
        
        # Создаем новую игру
        game = PokerGame([f"user_{user_id}", "AI_Fish"])
        game.start_hand()
        game.post_blinds()
        
        # Сохраняем игру
        self.active_games[user_id] = game
        
        # Показываем карты пользователя
        user_cards = game.player_cards[f"user_{user_id}"]
        
        await update.message.reply_text(
            f"🎮 ТЕСТОВАЯ ИГРА!\n\n"
            f"🃏 Ваши карты: {user_cards[0]} {user_cards[1]}\n"
            f"💰 Ваш стек: {game.player_stacks[f'user_{user_id}']} BB\n"
            f"🏦 Текущий банк: {game.pot} BB\n\n"
            f"Выберите действие:"
        )
        
        # Показываем кнопки действий
        await self.show_game_actions(update, context, user_id)
    
    async def show_game_actions(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
        """Показать доступные действия в игре"""
        game = self.active_games.get(user_id)
        if not game:
            await update.message.reply_text("Игра не найдена. Начните новую игру.")
            return
        
        # Создаем inline-кнопки
        keyboard = [
            [InlineKeyboardButton("📥 Колл", callback_data="game_call")],
            [InlineKeyboardButton("📤 Рейз", callback_data="game_raise")],
            [InlineKeyboardButton("❌ Фолд", callback_data="game_fold")],
            [InlineKeyboardButton("⚖️ Чек", callback_data="game_check")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Определяем текущую улицу
        street = "Префлоп"
        if len(game.community_cards) >= 3:
            street = "Флоп"
        if len(game.community_cards) >= 4:
            street = "Терн"
        if len(game.community_cards) >= 5:
            street = "Ривер"
        
        # Отправляем сообщение с кнопками
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🎯 Текущая улица: {street}\n"
                 f"💰 Текущая ставка: {game.current_bet} BB\n"
                 f"Выберите действие:",
            reply_markup=reply_markup
        )
    
    async def handle_button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(update.effective_user.id)
        action = query.data
        
        game = self.active_games.get(user_id)
        if not game:
            await query.edit_message_text("Игра не найдена. Начните новую игру командой /test_game")
            return
        
        # Обрабатываем действия
        if action == "game_fold":
            await self.handle_fold(query, user_id)
        elif action == "game_call":
            await self.handle_call(query, user_id, context)
        elif action == "game_check":
            await self.handle_check(query, user_id)
        elif action == "game_raise":
            await self.handle_raise_prompt(query, user_id)
    
    async def handle_fold(self, query, user_id):
        """Обработка фолда"""
        game = self.active_games[user_id]
        
        await query.edit_message_text(
            f"❌ Вы сбросили карты.\n"
            f"Игра завершена. Банк достается оппоненту.\n\n"
            f"Для новой игры используйте /test_game"
        )
        
        # Удаляем завершенную игру
        del self.active_games[user_id]
    
    async def handle_call(self, query, user_id, context: ContextTypes.DEFAULT_TYPE):
        """Обработка колла"""
        game = self.active_games[user_id]
        player = f"user_{user_id}"
        
        call_amount = game.current_bet
        game.player_stacks[player] -= call_amount
        game.pot += call_amount
        
        # Простая логика AI - всегда колл
        ai_player = "AI_Fish"
        game.player_stacks[ai_player] -= call_amount
        game.pot += call_amount
        
        response_text = (
            f"📥 Вы поставили {call_amount} BB\n"
            f"🤖 AI: колл\n\n"
            f"💰 Банк: {game.pot} BB\n"
            f"💵 Ваш стек: {game.player_stacks[player]} BB"
        )
        
        # Продолжаем игру - раздаем следующую улицу
        if len(game.community_cards) == 0:
            game.deal_flop()
            response_text += f"\n\n🃏 Флоп: {' '.join(str(card) for card in game.community_cards)}"
        elif len(game.community_cards) == 3:
            game.deal_turn()
            response_text += f"\n\n🃏 Терн: {game.community_cards[-1]}"
        elif len(game.community_cards) == 4:
            game.deal_river()
            response_text += f"\n\n🃏 Ривер: {game.community_cards[-1]}"
        else:
            # Шоудаун - определяем победителя
            winners = game.get_winner()
            response_text += f"\n\n🏆 Победитель: {winners[0] if 'user' in winners[0] else 'AI'}"
            response_text += f"\n🎯 Комбинация: {game.evaluate_showdown()[winners[0]][0].name}"
            del self.active_games[user_id]
            await query.edit_message_text(response_text)
            return
        
        await query.edit_message_text(response_text)
        
        # Показываем новые кнопки действий для следующей улицы
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Выберите следующее действие:"
        )
        await self.show_game_actions_by_chat(context, query.message.chat_id, user_id)
    
    async def show_game_actions_by_chat(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: str):
        """Показать кнопки действий по chat_id"""
        game = self.active_games.get(user_id)
        if not game:
            return
        
        keyboard = [
            [InlineKeyboardButton("📥 Колл", callback_data="game_call")],
            [InlineKeyboardButton("📤 Рейз", callback_data="game_raise")],
            [InlineKeyboardButton("❌ Фолд", callback_data="game_fold")],
            [InlineKeyboardButton("⚖️ Чек", callback_data="game_check")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text="Выберите действие:",
            reply_markup=reply_markup
        )
    
    async def handle_check(self, query, user_id):
        """Обработка чека"""
        await query.edit_message_text(
            "⚖️ Вы пропустили ход\n"
            "🤖 AI: чек\n\n"
            "Улица завершена, переходим к следующей..."
        )
        # Здесь будет логика продолжения игры
    
    async def handle_raise_prompt(self, query, user_id):
        """Запрос размера рейза"""
        await query.edit_message_text(
            "📤 Введите размер рейза (в BB):\n"
            "Например: 10\n\n"
            "Или отправьте 'отмена' для возврата к действиям"
        )
        # Здесь будем ждать ввод пользователя

    # ... остальные методы (show_help, settings, handle_message и т.д.) остаются без изменений ...
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
🤖 Poker Mentor - Помощь

Основные команды:
/start - Начать работу с ботом
/help - Показать эту справку
/settings - Показать настройки
/test_game - Быстро начать тестовую игру

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
            "Используйте команду /test_game для быстрого тестирования игровой логики."
        )
    
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