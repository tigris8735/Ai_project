import os
import logging
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

def create_app(bot_application):
    app = Flask(__name__)
    
    @app.route('/webhook', methods=['POST'])
    async def webhook():
        try:
            json_data = request.get_json()
            logger.info("📨 Получено сообщение от Telegram")
            
            from telegram import Update
            update = Update.de_json(json_data, bot_application.bot)
            await bot_application.process_update(update)
            
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return jsonify({"status": "error"}), 500
    
    @app.route('/')
    def home():
        return """
        <html>
            <head><title>Poker Mentor Bot</title></head>
            <body>
                <h1>🎲 Poker Mentor Bot</h1>
                <p>✅ Бот работает на Railway!</p>
                <p><a href="/health">Проверить статус</a></p>
            </body>
        </html>
        """
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "poker-bot"})
    
    return app