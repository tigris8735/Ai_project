#!/usr/bin/env python3
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Добавляем папку app в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def main():
    print("🎮 Poker Mentor Bot - Запуск на Railway...")
    print("=" * 50)
    
    try:
        from app.bot import PokerMentorBot
        from app.config import config
        from app.webhook_server import create_app
        
        # Инициализируем бота
        bot = PokerMentorBot()
        print("✅ Бот инициализирован")
        
        # Получаем конфигурацию webhook
        webhook_host = os.getenv('RAILWAY_STATIC_URL')
        if not webhook_host:
            # Если Railway не предоставил URL, используем дефолтный
            webhook_host = f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN')}" if os.getenv('RAILWAY_PUBLIC_DOMAIN') else None
        
        if webhook_host:
            print(f"🌐 Обнаружен Railway URL: {webhook_host}")
            
            # Настраиваем webhook
            webhook_url = f"{webhook_host}/webhook"
            secret_token = os.getenv('WEBHOOK_SECRET', 'default_railway_secret')
            
            import asyncio
            
            async def setup_webhook():
                try:
                    # Удаляем старый webhook если есть
                    await bot.application.bot.delete_webhook()
                    
                    # Устанавливаем новый webhook
                    result = await bot.application.bot.set_webhook(
                        url=webhook_url,
                        secret_token=secret_token,
                        max_connections=40,
                        allowed_updates=["message", "callback_query"]
                    )
                    
                    if result:
                        print(f"✅ Webhook установлен: {webhook_url}")
                        
                        # Проверяем информацию о webhook
                        webhook_info = await bot.application.bot.get_webhook_info()
                        print(f"📊 Webhook info: {webhook_info.url}")
                    else:
                        print("❌ Ошибка установки webhook")
                        
                except Exception as e:
                    print(f"❌ Ошибка настройки webhook: {e}")
                    # Продолжаем работу даже если webhook не установился
            
            # Запускаем настройку webhook
            asyncio.run(setup_webhook())
            
            # Создаем и запускаем Flask приложение
            flask_app = create_app(bot.application)
            
            port = int(os.getenv('PORT', 8000))
            host = '0.0.0.0'
            
            print(f"🚀 Запуск веб-сервера на {host}:{port}")
            print("📧 Бот готов принимать сообщения!")
            
            # Запускаем Flask (Railway сам управляет процессом)
            flask_app.run(host=host, port=port, debug=False)
            
        else:
            print("❌ Не удалось определить URL для webhook")
            print("🔄 Запуск в polling режиме...")
            bot.run()
            
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()