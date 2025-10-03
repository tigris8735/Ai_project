import os
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application

logger = logging.getLogger(__name__)

def create_app(bot_application):
    app = Flask(__name__)
    
    @app.route('/webhook', methods=['POST'])
    async def webhook():
        try:
            json_data = request.get_json()
            logger.info(f"Received update: {json_data}")
            
            update = Update.de_json(json_data, bot_application.bot)
            await bot_application.process_update(update)
            
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route('/')
    def home():
        return """
        <html>
            <head>
                <title>Poker Mentor Bot</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .container { max-width: 600px; margin: 0 auto; }
                    .status { color: green; font-weight: bold; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎲 Poker Mentor Bot</h1>
                    <p class="status">✅ Бот работает и готов к работе!</p>
                    <p>Бот успешно развернут на Railway и ожидает сообщений от Telegram.</p>
                    <p><a href="/health">Проверить статус</a></p>
                </div>
            </body>
        </html>
        """
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy", 
            "service": "poker-mentor-bot",
            "version": "1.0"
        })
    
    return app