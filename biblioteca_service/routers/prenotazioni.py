from fastapi import APIRouter, Depends
from config.database import get_db
from services.prenotazione_service import PrenotazioneService
from schemas.prenotazione_schemas import PrenotazioneCreate, PrenotazioneResponse

router = APIRouter(prefix="/prenotazioni", tags=["prenotazioni"])

@router.get("/")
def get_prenotazioni(db=Depends(get_db)):
    return PrenotazioneService.get_all_prenotazioni(db)

@router.get("/{prenotazione_id}")
def get_prenotazione(prenotazione_id: int, db=Depends(get_db)):
    return PrenotazioneService.get_prenotazione_by_id(db, prenotazione_id)

@router.post("/", status_code=201)
def create_prenotazione(prenotazione_data: PrenotazioneCreate, db=Depends(get_db)):
    return PrenotazioneService.create_prenotazione(db, prenotazione_data)

@router.delete("/{prenotazione_id}", status_code=204)
def delete_prenotazione(prenotazione_id: int, db=Depends(get_db)):
    PrenotazioneService.delete_prenotazione(db, prenotazione_id)
    return None
