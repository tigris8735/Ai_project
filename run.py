import os
import sys
import logging
import asyncio
from flask import Flask, request, jsonify

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = None

try:
    from app.bot import PokerMentorBot
    bot = PokerMentorBot()
    logger.info("✅ БОТ ЗАГРУЖЕН НАХУЙ!")
except Exception as e:
    logger.error(f"💥 БОТ НЕ ГРУЗИТСЯ: {e}")

@app.route('/')
def home():
    return """
    <h1>🎲 POKER BOT АКТИВЕН!</h1>
    <p>Напиши /start в Telegram, сука!</p>
    """

@app.route('/health')
def health():
    return jsonify({"status": "WORKING", "bot": "READY"})

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not bot:
            return jsonify({"error": "Bot not loaded"}), 500
            
        data = request.get_json()
        logger.info(f"📨 Получено сообщение: {data}")
        
        # Асинхронно обрабатываем
        async def process():
            from telegram import Update
            update = Update.de_json(data, bot.application.bot)
            await bot.application.process_update(update)
        
        asyncio.run(process())
        return jsonify({"status": "processed"})
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return jsonify({"error": str(e)}), 500

# Устанавливаем вебхук при старте
if bot:
    @app.before_first_request
    def setup_webhook():
        try:
            railway_url = "https://aproject-production-3cfa.up.railway.app"
            
            async def set_wh():
                await bot.application.bot.delete_webhook()
                result = await bot.application.bot.set_webhook(
                    url=f"{railway_url}/webhook",
                    secret_token=os.getenv('WEBHOOK_SECRET', 'ebuchiy_secret')
                )
                if result:
                    logger.info("✅ ВЕБХУК УСТАНОВЛЕН!")
                else:
                    logger.error("❌ ВЕБХУК НЕ УСТАНОВИЛСЯ!")
            
            asyncio.run(set_wh())
        except Exception as e:
            logger.error(f"💥 Вебхук не поставился: {e}")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    logger.info(f"🚀 ЗАПУСКАЕМСЯ НА ПОРТУ {port}")
    app.run(host='0.0.0.0', port=port, debug=False)