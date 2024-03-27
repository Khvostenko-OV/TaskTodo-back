import os

from dotenv import load_dotenv

load_dotenv(verbose=False, override=True)  # take environment variables from .env

# Postgres local
DB_NAME = os.getenv('DB_NAME', 'db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', 5432)


# Flask
class Config:
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY = os.getenv('SECRET_KEY', 'EWSCVBHYTRE$%^%$#@TGVCXCVBNHT')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = Config()

# Pagination
DEFAULT_PAGE_LIMIT = os.getenv("DEFAULT_PAGE_LIMIT", 3)
