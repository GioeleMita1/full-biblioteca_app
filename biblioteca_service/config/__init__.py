"""
Configurazione dell'applicazione
"""
from .database_config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DATABASE_URL
)

__all__ = [
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "DATABASE_URL"
]
