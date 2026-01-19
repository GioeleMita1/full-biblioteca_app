"""
Repository per l'accesso ai dati
"""
from .user_repository import UserRepository
from .libro_repository import LibroRepository
from .prenotazione_repository import PrenotazioneRepository

__all__ = ["UserRepository", "LibroRepository", "PrenotazioneRepository"]
