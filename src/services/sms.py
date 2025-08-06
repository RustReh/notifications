import httpx
from ..gateway.interfaces import NotificationService
from ..schemas.request_schema import NotificationRequest
from ..utils.exceptions import NotificationError


class SMSService:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

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