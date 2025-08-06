import httpx

from ..schemas.request_schema import NotificationRequest
from ..utils.exceptions import NotificationError

class TelegramService:
    def __init__(self, bot_token: str):
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    async def send_message(self, chat_id: str, request: NotificationRequest) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json={
                        "chat_id": chat_id,
                        "text": request.message,
                        "parse_mode": "Markdown"
                    }
                )
                if response.status_code != 200:
                    raise NotificationError(f"Telegram API error: {response.text}")
                return True
        except httpx.HTTPError as e:
            raise NotificationError(f"Telegram connection error: {str(e)}")