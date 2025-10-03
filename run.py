from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🎲 POKER BOT РАБОТАЕТ НАХУЙ! 🎲"

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)