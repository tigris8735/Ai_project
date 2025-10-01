# Здесь я напишу все нужные библиотеки и фреймворки 

# Графический интерфейс приложения : 

PyQt6>=6.6.0
PyQt6-WebEngine>=6.6.0  # Для встроенного браузера/чата
qt-material>=2.14.0     # Material Design темы для PyQt

**Альтернатива - Tkinter (входит в стандартную библиотеку)**

tkinter                # Базовый GUI (если выберем его вместо PyQt)
Kivy                   # Кроссплатформенный GUI (если решим делать крассплат. приложение)


# Backend и Api

**Асинхронный фреймворк**
fastapi>=0.104.0
uvicorn>=0.24.0         # ASGI сервер
python-multipart>=0.0.6 # Для работы с формами

**HTTP клиенты**
aiohttp>=3.9.0          # Асинхронные HTTP запросы
requests>=2.31.0        # Синхронные HTTP запросы
httpx>=0.25.0           # Альтернативный async HTTP клиент


# Базы данных и ORM 

**SQL база данных**
sqlalchemy>=2.0.0
alembic>=1.12.0         # Миграции базы данных

SQLite (входит в стандартную библиотеку)
sqlite3

**Векторная база данных**
chromadb>=0.4.0
faiss-cpu>=1.7.4        # Для семантического поиска (альтернатива)

**Кэширование**
redis>=5.0.0            # Если будем использовать Redis


# AI и ml (машинное обучение)

**OpenAI**
openai>=1.3.0

**Anthropic Claude**
anthropic>=0.7.0

**Локальные модели**
ollama>=0.1.0           # Для работы с локальными моделями
transformers>=4.35.0    # Hugging Face трансформеры
torch>=2.0.0            # PyTorch для локальных моделей



# Обработка текста и эмбеддинг

**Эмбеддинги и NLP**
sentence-transformers>=2.2.0
nltk>=3.8.0             # Обработка естественного языка
spacy>=3.7.0            # Продвинутая NLP
langchain>=0.0.350      # Фреймворк для AI приложений

**Токенизация**
tiktoken>=0.5.0         # Токенизатор OpenAI


# Data science и анализ 

**Анализ данных**
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0

**Машинное обучение**
scikit-learn>=1.3.0
matplotlib>=3.7.0       # Визуализация данных
seaborn>=0.13.0         # Статистическая визууализация
plotly>=5.17.0          # Интерактивные графики


# Парсинг и обработка данных
## Парсинг hand history
**Регулярные выражения (входит в стандартную библиотеку)**
re

**Парсинг текста**
lxml>=4.9.0             # Парсинг HTML/XML
beautifulsoup4>=4.12.0  # Парсинг HTML
html5lib>=1.1           # Парсер HTML

**Обработка дат**
python-dateutil>=2.8.0
pytz>=2023.0            # Часовые пояса

## Работа с файлами

**JSON (входит в стандартную библиотеку)**
json
**CSV (входит в стандартную библиотеку)**
csv
**Конфигурации**
pyyaml>=6.0             # YAML конфиги
toml>=0.10.0            # TOML конфиги

**Работа с путями**
pathlib2>=2.3.0         # Если нужна обратная совместимость

# Утилиты и вспомогательные библиотеки
## Системные утилиты

**Асинхронное программирование**
asyncio                 # Входит в стандартную библиотеку
concurrent.futures      # Входит в стандартную библиотеку

**Логирование**
logging                 # Входит в стандартную библиотеку
loguru>=0.7.0           # Удобное логирование

**Конфигурация**
pydantic>=2.0.0         # Валидация данных
pydantic-settings>=2.0.0 # Управление настройками

## Безопасность

**Шифрование и безопасность**
cryptography>=41.0.0    # Шифрование данных
python-jose>=3.3.0      # JWT токены
passlib>=1.7.4          # Хэширование паролей
bcrypt>=4.0.0           # Хэширование

## Производительность

**Оптимизация**
psutil>=5.9.0           # Мониторинг системы
numexpr>=2.8.0          # Ускорение вычислений

# Тестирование и разработка
## Тестирование

pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-qt>=4.2.0        # Тестирование PyQt
pytest-cov>=4.1.0       # Покрытие кода
hypothesis>=6.82.0      # Property-based testing

## Инструменты разработки

**Code quality**
black>=23.0.0           # Форматирование кода
flake8>=6.0.0           # Линтинг
mypy>=1.0.0             # Статическая типизация
pre-commit>=3.0.0       # Pre-commit хуки

**Документация**
sphinx>=7.0.0           # Генерация документации
mkdocs>=1.5.0           # Documentation site


# Специфичные для покера
## Покерные вычисления

**Покерная математика**
pokerlib>=2.0.0         # Покерные утилиты (если найдем хорошую)
deuces>=0.2.0           # Оценка покерных рук

## Файл requirements.txt

**GUI**
PyQt6>=6.6.0
PyQt6-WebEngine>=6.6.0
qt-material>=2.14.0

**Backend**
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
aiohttp>=3.9.0
requests>=2.31.0

**Database**
sqlalchemy>=2.0.0
alembic>=1.12.0
chromadb>=0.4.0

**AI/ML**
openai>=1.3.0
anthropic>=0.7.0
sentence-transformers>=2.2.0
transformers>=4.35.0
torch>=2.0.0
ollama>=0.1.0
langchain>=0.0.350
tiktoken>=0.5.0

**Data Analysis**
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
plotly>=5.17.0

**Utilities**
python-dateutil>=2.8.0
pytz>=2023.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
loguru>=0.7.0
pyyaml>=6.0

**Parsing**
lxml>=4.9.0
beautifulsoup4>=4.12.0

**Testing**
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-qt>=4.2.0