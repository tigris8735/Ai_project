import os
import sys
import logging
import asyncio
from threading import Thread

# Добавляем app в путь
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_flask():
    """Запускаем Flask для health checks"""
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return """
        <html>
            <head><title>Poker Bot</title></head>
            <body>
                <h1>🎲 POKER BOT РАБОТАЕТ!</h1>
                <p>Бот запущен и готов к работе!</p>
                <p>Напиши /start в Telegram</p>
                <p><a href="/health">Проверить статус</a></p>
            </body>
        </html>
        """
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy", 
            "bot": "running",
            "message": "Бот работает!"
        })
    
    port = int(os.getenv('PORT', 8000))
    logger.info(f"🌐 Веб-сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

def run_bot():
    """Запускаем бота"""
    try:
        logger.info("🚀 ЗАПУСКАЕМ БОТА!")
        
        from app.bot import PokerMentorBot
        bot = PokerMentorBot()
        
        logger.info("✅ БОТ ИНИЦИАЛИЗИРОВАН!")
        logger.info("🤖 Бот готов принимать сообщения!")
        
        # Запускаем бота (polling режим)
        bot.run()
        
    except Exception as e:
        logger.error(f"💥 ОШИБКА БОТА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    logger.info("🎯 ЗАПУСКАЕМ СИСТЕМУ!")
    
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Запускаем бота в основном потоке
    run_bot()