import os
import sys
import logging
from threading import Thread

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_flask():
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "POKER BOT РАБОТАЕТ! Напиши /start в Telegram"
    
    @app.route('/health')
    def health():
        return "OK"
    
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)

def run_bot():
    try:
        from app.bot import PokerMentorBot
        bot = PokerMentorBot()
        logger.info("✅ БОТ ЗАПУЩЕН!")
        bot.run()
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    run_bot()