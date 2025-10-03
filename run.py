import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверяем зависимости
try:
    import telegram
    logger.info("✅ telegram module FOUND")
except ImportError as e:
    logger.error(f"❌ NO telegram module: {e}")

try:
    import flask
    logger.info("✅ flask module FOUND") 
except ImportError as e:
    logger.error(f"❌ NO flask module: {e}")

try:
    import sqlalchemy
    logger.info("✅ sqlalchemy module FOUND")
except ImportError as e:
    logger.error(f"❌ NO sqlalchemy module: {e}")

# Простой сервер чтобы проверить что все работает
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "CHECKING DEPENDENCIES..."

@app.route('/health')
def health():
    return "DEPENDENCY CHECK"

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    logger.info(f"Starting test server on port {port}")
    app.run(host='0.0.0.0', port=port)