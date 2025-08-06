from typing import Protocol, runtime_checkable

@runtime_checkable
class NotificationService(Protocol):
    async def send_message(self, recipient: str, message: str, **kwargs) -> bool:
        """Асинхронная отправка уведомления"""
        ...