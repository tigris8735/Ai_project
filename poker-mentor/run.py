#!/usr/bin/env python3
import sys
import os
import logging
from app.config import config

# Добавляем папку app в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def setup_webhook_config():
    """Настройка конфигурации для webhook режима"""
    webhook_config = {
        'WEBHOOK_HOST': os.getenv('WEBHOOK_HOST', 'https://yourdomain.com'),
        'WEBHOOK_PORT': int(os.getenv('WEBHOOK_PORT', 8443)),
        'WEBHOOK_PATH': os.getenv('WEBHOOK_PATH', '/webhook'),
        'WEBHOOK_SECRET': os.getenv('WEBHOOK_SECRET', 'your_secret_token_here'),
        'SSL_CERT_PATH': os.getenv('SSL_CERT_PATH', '/path/to/cert.pem'),
        'SSL_KEY_PATH': os.getenv('SSL_KEY_PATH', '/path/to/private.key')
    }
    
    # Проверяем обязательные настройки для production
    if not webhook_config['WEBHOOK_HOST'].startswith('https://'):
        logging.warning("WEBHOOK_HOST должен использовать HTTPS для production")
    
    return webhook_config

def main():
    """Главная функция запуска с поддержкой webhook"""
    print("🎮 Poker Mentor Bot - Запуск...")
    print("=" * 50)
    
    try:
        # Проверяем режим запуска
        run_mode = os.getenv('RUN_MODE', 'polling').lower()
        
        if run_mode == 'webhook':
            print("🌐 Режим: WEBHOOK")
            from app.bot import PokerMentorBot
            from app.webhook_server import WebhookServer
            
            # Создаем бота
            bot = PokerMentorBot()
            
            # Настраиваем webhook
            webhook_config = setup_webhook_config()
            webhook_url = f"{webhook_config['WEBHOOK_HOST']}{webhook_config['WEBHOOK_PATH']}"
            
            # Устанавливаем webhook в Telegram
            import asyncio
            async def setup_webhook():
                await bot.application.bot.set_webhook(
                    url=webhook_url,
                    secret_token=webhook_config['WEBHOOK_SECRET'],
                    max_connections=40
                )
                print(f"✅ Webhook установлен: {webhook_url}")
            
            asyncio.run(setup_webhook())
            
            # Создаем и запускаем webhook сервер
            server = WebhookServer(
                bot_application=bot.application,
                host='0.0.0.0',
                port=webhook_config['WEBHOOK_PORT']
            )
            
            # Настраиваем SSL контекст
            ssl_context = None
            if os.path.exists(webhook_config['SSL_CERT_PATH']) and os.path.exists(webhook_config['SSL_KEY_PATH']):
                ssl_context = (webhook_config['SSL_CERT_PATH'], webhook_config['SSL_KEY_PATH'])
                print("🔐 SSL контекст загружен")
            else:
                print("⚠️  SSL сертификаты не найдены, запуск без HTTPS")
            
            print("🤖 Webhook сервер запускается...")
            server.run(ssl_context=ssl_context)
            
        else:
            # Режим polling (по умолчанию)
            print("🔄 Режим: POLLING")
            from app.bot import PokerMentorBot
            
            bot = PokerMentorBot()
            print("✅ Бот создан успешно")
            print("🤖 Бот запускается в polling режиме...")
            print("🛑 Для остановки нажмите Ctrl+C")
            print("=" * 50)
            
            bot.run()
        
    except KeyboardInterrupt:
        print("\n👋 До свидания! Бот остановлен.")
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()