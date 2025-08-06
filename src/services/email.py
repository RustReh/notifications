import aiosmtplib
from email.mime.text import MIMEText
from ..schemas.request_schema import NotificationRequest
from ..utils.exceptions import NotificationError
from src.settings import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD

    async def send_message(self, recipient: str, request: NotificationRequest) -> bool:
        try:
            message = MIMEText(request.message)
            message["From"] = self.username
            message["To"] = recipient
            message["Subject"] = request.subject or "Notification"

            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                use_tls=True
            )
            return True
        except Exception as e:
            raise NotificationError(f"Email error: {str(e)}")