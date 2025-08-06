from typing import Any


class NotificationError(Exception):
    default_detail = "Notification service error"
    default_code = "invalid"

    def __init__(
            self,
            code: str | None = None,
            detail: str | None = None,
            **kwargs: Any,
    ) -> None:
        self.code = code if code else self.default_code
        self.detail = detail if detail else self.default_detail
        self.kwargs = kwargs