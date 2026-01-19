# Repository per Prenotazione
from sqlalchemy.orm import Session
from models.prenotazione import Prenotazione
from datetime import datetime

class PrenotazioneRepository:

    @staticmethod
    def get_all(db):
        return db.query(Prenotazione).all()

    @staticmethod
    def get_by_id(db, prenotazione_id):
        return db.query(Prenotazione).filter(Prenotazione.id == prenotazione_id).first()

    @staticmethod
    def check_libro_disponibile(db, libro_id, data_inizio, data_fine):
        prenotazioni = db.query(Prenotazione).filter(Prenotazione.libro_id == libro_id, Prenotazione.stato == "attiva", Prenotazione.data_inizio < data_fine, Prenotazione.data_fine > data_inizio).all()
        return len(prenotazioni) == 0

    @staticmethod
    def create(db, prenotazione_data):
        prenotazione = Prenotazione(**prenotazione_data)
        db.add(prenotazione)
        db.commit()
        db.refresh(prenotazione)
        return prenotazione

    @staticmethod
    def delete(db, prenotazione):
        db.delete(prenotazione)
        db.commit()
