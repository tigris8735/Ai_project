#!/usr/bin/env python3
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(__file__))

print("🔧 Импортируем модули...")

try:
    # Проверяем основные импорты
    from app.bot import PokerMentorBot
    from app.config import config
    print("✅ Основные модули загружены")
    
    # Пропускаем проблемные ML модули на первое время
    print("⚠️ Пропускаем ML модули для первого запуска")
    
except ImportError as e:
    print(f"⚠️ Предупреждение: {e}")
    # Продолжаем без некоторых модулей

def main():
    print("🎮 Poker Mentor Bot - Запуск на Railway...")
    
    try:
        from app.bot import PokerMentorBot
        from app.webhook_server import create_app
        
        # Инициализируем бота
        bot = PokerMentorBot()
        print("✅ Бот инициализирован")
        
        # Получаем URL Railway
        railway_url = os.getenv('RAILWAY_STATIC_URL') 
        if not railway_url and os.getenv('RAILWAY_PUBLIC_DOMAIN'):
            railway_url = f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN')}"
        
        if railway_url:
            print(f"🌐 Railway URL: {railway_url}")
            
            # Настраиваем webhook
            webhook_url = f"{railway_url}/webhook"
            secret_token = os.getenv('WEBHOOK_SECRET', 'railway_secret_123')
            
            import asyncio
            
            async def setup_webhook():
                try:
                    await bot.application.bot.delete_webhook()
                    result = await bot.application.bot.set_webhook(
                        url=webhook_url,
                        secret_token=secret_token,
                        max_connections=40
                    )
                    if result:
                        print(f"✅ Webhook установлен: {webhook_url}")
                        
                        # Проверяем webhook info
                        webhook_info = await bot.application.bot.get_webhook_info()
                        print(f"📊 Webhook info: {webhook_info.url}")
                    else:
                        print("❌ Ошибка установки webhook")
                except Exception as e:
                    print(f"⚠️ Ошибка webhook: {e}")
                    # Продолжаем работу даже если webhook не установился
            
            asyncio.run(setup_webhook())
            
            # Запускаем Flask
            flask_app = create_app(bot.application)
            port = int(os.getenv('PORT', 8000))
            
            print(f"🚀 Сервер запущен на порту {port}")
            print("📱 Бот готов к работе!")
            flask_app.run(host='0.0.0.0', port=port, debug=False)
            
        else:
            print("❌ Не удалось определить URL Railway")
            print("🔄 Запуск в polling режиме...")
            bot.run()
            
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()