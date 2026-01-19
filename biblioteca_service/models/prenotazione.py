# entità prenotazione
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Prenotazione(Base):
    __tablename__ = "prenotazioni"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libri.id"), nullable=False)
    data_inizio = Column(DateTime(timezone=True), nullable=False)
    data_fine = Column(DateTime(timezone=True), nullable=False)
    stato = Column(String, default="attiva", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    utente = relationship("User", back_populates="prenotazioni")
    libro = relationship("Libro", back_populates="prenotazioni")
