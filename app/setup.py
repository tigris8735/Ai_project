from setuptools import setup, find_packages

setup(
    name="poker-bot",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot[job-queue]==20.7",
        "sqlalchemy==2.0.23", 
        "flask==2.3.3",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "numpy==1.24.3",
        "alembic==1.12.1"
    ]
)