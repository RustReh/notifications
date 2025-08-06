from typing import Protocol, runtime_checkable

from src.schemas.request_schema import NotificationRequest


@runtime_checkable
class NotificationService(Protocol):
    async def send_message(self, recipient: str, request: NotificationRequest) -> bool:
        """Асинхронная отправка уведомления"""
        ...