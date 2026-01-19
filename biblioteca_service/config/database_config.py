import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5434"))
DB_USER = os.getenv("DB_USER", "biblioteca_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "biblioteca_password")
DB_NAME = os.getenv("DB_NAME", "biblioteca_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
