from pydantic import BaseModel

class EmailRequest(BaseModel):
    emailType: str
    recipientEmail: str
    nome: str | None = None
    titoloLibro: str | None = None
    data: str | None = None
