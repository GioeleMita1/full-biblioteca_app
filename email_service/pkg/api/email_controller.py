from fastapi import APIRouter
from pkg.model.email_request import EmailRequest
from pkg.services.email_services import EmailService

router = APIRouter(prefix="/api/internal/emails", tags=["Emails"])

@router.post("/send/v1", status_code=200)
def send_email(request: EmailRequest):
    result = EmailService.send_email(request)
    return result
