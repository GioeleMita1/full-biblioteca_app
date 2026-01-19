import os
from email.mime.text import MIMEText
import smtplib
from pkg.model.email_request import EmailRequest
from pkg.config.settings import SENDER_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

# cartella template (templetes per typo)
TEMPLATE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/templetes"

class EmailService:

    @staticmethod
    def render_template(request):
        if request.emailType == "RESERVE":
            template_file = TEMPLATE_DIR + "/reserve_email.txt"
        elif request.emailType == "RETURN":
            template_file = TEMPLATE_DIR + "/return_email.txt"
        else:
            return "Errore: tipo email sconosciuto"
        with open(template_file, "r", encoding="utf-8") as f:
            template_text = f.read()
        email_text = template_text
        if request.nome:
            email_text = email_text.replace("{{nome}}", request.nome)
        if request.titoloLibro:
            email_text = email_text.replace("{{titoloLibro}}", request.titoloLibro)
        if request.data:
            email_text = email_text.replace("{{data}}", request.data)
        return email_text

    @staticmethod
    def send_email(request):
        email_content = EmailService.render_template(request)
        msg = MIMEText(email_content)
        msg["Subject"] = request.emailType + " - Notifica"
        msg["From"] = SENDER_EMAIL
        msg["To"] = request.recipientEmail
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            return {"status": "ok", "message": "Email inviata a " + request.recipientEmail}
        except Exception as e:
            return {"status": "error", "message": str(e)}
