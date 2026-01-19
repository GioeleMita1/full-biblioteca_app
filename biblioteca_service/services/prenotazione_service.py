# service per prenotazione
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.prenotazione_repository import PrenotazioneRepository
from repositories.libro_repository import LibroRepository
from repositories.user_repository import UserRepository
from schemas.prenotazione_schemas import PrenotazioneCreate, PrenotazioneResponse
from services.sns_publisher import publish_email_event

def _format_data(dt):
    if dt == None:
        return ""
    return dt.strftime("%d/%m/%Y") if hasattr(dt, "strftime") else str(dt)

class PrenotazioneService:

    @staticmethod
    def get_all_prenotazioni(db):
        prenotazioni = PrenotazioneRepository.get_all(db)
        return [PrenotazioneResponse.model_validate(p) for p in prenotazioni]

    @staticmethod
    def get_prenotazione_by_id(db, prenotazione_id):
        prenotazione = PrenotazioneRepository.get_by_id(db, prenotazione_id)
        if prenotazione == None:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        return PrenotazioneResponse.model_validate(prenotazione)

    @staticmethod
    def create_prenotazione(db, prenotazione_data):
        user = UserRepository.get_by_id(db, prenotazione_data.user_id)
        if user == None:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        libro = LibroRepository.get_by_id(db, prenotazione_data.libro_id)
        if libro == None:
            raise HTTPException(status_code=404, detail="Libro non trovato")
        if PrenotazioneRepository.check_libro_disponibile(db, prenotazione_data.libro_id, prenotazione_data.data_inizio, prenotazione_data.data_fine) == False:
            raise HTTPException(status_code=400, detail="Libro già prenotato per questo periodo")
        created = PrenotazioneRepository.create(db, prenotazione_data.model_dump())
        publish_email_event({"emailType": "RESERVE", "recipientEmail": user.email, "nome": user.nome, "titoloLibro": libro.titolo, "data": _format_data(prenotazione_data.data_inizio)})
        return PrenotazioneResponse.model_validate(created)

    @staticmethod
    def delete_prenotazione(db, prenotazione_id):
        prenotazione = PrenotazioneRepository.get_by_id(db, prenotazione_id)
        if prenotazione == None:
            raise HTTPException(status_code=404, detail="Prenotazione non trovata")
        email = prenotazione.utente.email
        nome = prenotazione.utente.nome
        titolo_libro = prenotazione.libro.titolo
        data = _format_data(prenotazione.data_fine)
        PrenotazioneRepository.delete(db, prenotazione)
        publish_email_event({"emailType": "RETURN", "recipientEmail": email, "nome": nome, "titoloLibro": titolo_libro, "data": data})
