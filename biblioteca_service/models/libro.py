# entità libro
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Libro(Base):
    __tablename__ = "libri"
    id = Column(Integer, primary_key=True, index=True)
    titolo = Column(String, nullable=False)
    autore = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False, index=True)
    disponibile = Column(Boolean, default=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    utente = relationship("User", back_populates="libri")
    prenotazioni = relationship("Prenotazione", back_populates="libro")
