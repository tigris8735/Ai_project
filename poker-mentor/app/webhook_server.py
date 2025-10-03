import logging
import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, ContextTypes

logger = logging.getLogger(__name__)

class WebhookServer:
    def __init__(self, bot_application: Application, host: str = '0.0.0.0', port: int = 8443):
        self.bot_app = bot_application
        self.host = host
        self.port = port
        self.flask_app = Flask(__name__)
        self._setup_routes()
        
    def _setup_routes(self):
        """Настройка маршрутов Flask"""
        
        @self.flask_app.route('/webhook', methods=['POST'])
        async def webhook():
            """Основной webhook endpoint"""
            try:
                # Получаем данные от Telegram
                json_data = request.get_json()
                logger.debug(f"Received update: {json_data}")
                
                # Создаем объект Update
                update = Update.de_json(json_data, self.bot_app.bot)
                
                # Передаем в обработчики бота
                await self.bot_app.process_update(update)
                
                return jsonify({"status": "ok"}), 200
                
            except Exception as e:
                logger.error(f"Webhook error: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
        
        @self.flask_app.route('/health', methods=['GET'])
        def health_check():
            """Health check для мониторинга"""
            return jsonify({
                "status": "healthy",
                "bot": "running",
                "webhook": "active"
            }), 200
        
        @self.flask_app.route('/set_webhook', methods=['POST'])
        async def set_webhook():
            """Установка webhook URL"""
            try:
                webhook_url = request.json.get('url')
                secret_token = os.getenv('WEBHOOK_SECRET', 'your_secret_token')
                
                # Устанавливаем webhook в Telegram
                result = await self.bot_app.bot.set_webhook(
                    url=webhook_url,
                    secret_token=secret_token,
                    max_connections=40
                )
                
                return jsonify({
                    "status": "success" if result else "failed",
                    "webhook_url": webhook_url
                }), 200
                
            except Exception as e:
                logger.error(f"Set webhook error: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

    def run(self, ssl_context=None):
        """Запуск Flask сервера"""
        logger.info(f"Starting webhook server on {self.host}:{self.port}")
        self.flask_app.run(
            host=self.host,
            port=self.port,
            ssl_context=ssl_context,
            debug=False
        )