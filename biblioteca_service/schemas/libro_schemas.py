from pydantic import BaseModel
from datetime import datetime

class LibroBase(BaseModel):
    titolo: str
    autore: str
    isbn: str

class LibroCreate(LibroBase):
    pass

class LibroResponse(LibroBase):
    id: int
    disponibile: bool
    user_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class LibroPresta(BaseModel):
    user_id: int
