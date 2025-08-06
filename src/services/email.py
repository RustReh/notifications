import aiosmtplib
from email.mime.text import MIMEText
from ..schemas.request_schema import NotificationRequest
from ..utils.exceptions import NotificationError

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

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