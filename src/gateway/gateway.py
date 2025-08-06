from ..schemas.request_schema import NotificationRequest
from ..utils.exceptions import NotificationError
from .interfaces import NotificationService

class NotificationGateway:
    def __init__(self):
        self._services: dict[str, NotificationService] = {}

    def register_service(self, name: str, service: NotificationService) -> None:
        if not isinstance(service, NotificationService):
            raise TypeError("Service must implement NotificationService protocol")
        self._services[name] = service

    async def send_with_fallback(self, request: NotificationRequest) -> bool:
        """Отправка с автоматическим переключением на резервные каналы"""
        errors = {}

        for channel in request.priority_order:
            if not getattr(request.contacts, channel, None):
                continue

            try:
                is_sent = await (
                    self._services[channel]
                    .send_message(getattr(request.contacts, channel), request.message)
                )
                return is_sent

            except NotificationError as e:
                errors[channel] = str(e)
                continue

        raise NotificationError(
            f"All channels failed: {errors}",
            fallback_errors=errors
        )
