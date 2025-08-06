import httpx

from ..schemas.request_schema import NotificationRequest
from ..utils.exceptions import NotificationError
from src.settings import settings


class SMSService:
    def __init__(self):
        self.api_url = settings.SMS_API_URL
        self.api_key = settings.SMS_API_KEY

    async def send_message(self, phone: str, request: NotificationRequest) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/send",
                    json={
                        "phone": phone,
                        "text": request.message,
                        "key": self.api_key
                    },
                    timeout=10.0
                )
                if response.status_code != 200:
                    raise NotificationError(f"SMS API error: {response.text}")
                return True
        except httpx.HTTPError as e:
            raise NotificationError(f"SMS connection error: {str(e)}")