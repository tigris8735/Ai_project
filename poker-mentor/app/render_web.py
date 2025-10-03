from flask import Flask
import subprocess
import threading
import os

app = Flask(__name__)

def run_bot():
    """Запуск бота в фоне"""
    try:
        subprocess.run(["python", "run.py"])
    except Exception as e:
        print(f"Bot error: {e}")

@app.route('/')
def home():
    return "Poker Mentor Bot is running!"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    # Запускаем бот в отдельном процессе
    bot_process = threading.Thread(target=run_bot, daemon=True)
    bot_process.start()
    
    # Запускаем веб-сервер
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)