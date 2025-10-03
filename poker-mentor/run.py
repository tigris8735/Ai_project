#!/usr/bin/env python3
import os
import sys
import logging

# Добавляем app в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🚀 Starting Poker Bot...")

try:
    # Проверяем базовые импорты
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return """
        <html>
            <head><title>Poker Bot</title></head>
            <body>
                <h1>🎲 Poker Mentor Bot</h1>
                <p>✅ Successfully deployed on Railway!</p>
                <p><a href="/health">Health Check</a></p>
            </body>
        </html>
        """
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "poker-bot"})
    
    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            # Простой webhook для теста
            data = request.get_json()
            logger.info(f"Received webhook: {data}")
            return jsonify({"status": "ok"})
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return jsonify({"status": "error"}), 500
    
    # Пробуем импортировать бота
    try:
        from app.bot import PokerMentorBot
        bot = PokerMentorBot()
        logger.info("✅ Bot initialized successfully")
        
        # Настраиваем webhook если есть URL
        railway_url = os.getenv('RAILWAY_STATIC_URL') 
        if railway_url:
            import asyncio
            
            async def setup_webhook():
                try:
                    webhook_url = f"{railway_url}/webhook"
                    await bot.application.bot.set_webhook(
                        url=webhook_url,
                        secret_token=os.getenv('WEBHOOK_SECRET', 'default_secret')
                    )
                    logger.info(f"✅ Webhook set: {webhook_url}")
                except Exception as e:
                    logger.error(f"❌ Webhook setup failed: {e}")
            
            asyncio.run(setup_webhook())
            
    except ImportError as e:
        logger.warning(f"⚠️ Could not import bot: {e}")
    except Exception as e:
        logger.error(f"❌ Bot initialization failed: {e}")
    
    # Запускаем сервер
    if __name__ == "__main__":
        port = int(os.getenv('PORT', 8000))
        logger.info(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    logger.error(f"💥 Critical error: {e}")
    import traceback
    traceback.print_exc()