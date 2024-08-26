# flaskConfig.py

import os

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'inventory_system')
DB_USER = os.environ.get('DB_USER', 'your_username')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'your_password')
DB_PORT = os.environ.get('DB_PORT', 5432)

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
DEBUG = os.environ.get('DEBUG', True)

# Other configurations
ITEMS_PER_PAGE = 10

# PostgreSQL connection string
POSTGRES_CONNECTION_STRING = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
