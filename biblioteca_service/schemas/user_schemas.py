from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    nome: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
