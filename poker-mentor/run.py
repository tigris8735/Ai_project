#!/usr/bin/env python3
"""
Poker Mentor Bot - Запускной файл
"""

import sys
import os

# Добавляем папку app в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def main():
    """Главная функция запуска"""
    print("🎮 Poker Mentor Bot")
    print("=" * 40)
    
    try:
        from app.bot import PokerMentorBot
        bot = PokerMentorBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 До свидания! Бот остановлен.")
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()