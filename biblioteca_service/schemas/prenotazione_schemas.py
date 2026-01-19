from pydantic import BaseModel
from datetime import datetime

class PrenotazioneBase(BaseModel):
    user_id: int
    libro_id: int
    data_inizio: datetime
    data_fine: datetime

class PrenotazioneCreate(PrenotazioneBase):
    pass

class PrenotazioneResponse(PrenotazioneBase):
    id: int
    stato: str
    created_at: datetime

    class Config:
        from_attributes = True
