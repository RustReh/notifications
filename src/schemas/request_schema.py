from pydantic import BaseModel, EmailStr, field_validator

class ContactData(BaseModel):
    """Валидация контактных данных"""
    email: EmailStr | None = None
    phone: str| None = None
    telegram: str | None = None

    @field_validator("phone")
    def validate_phone(cls, v):
        if v and not v.startswith('+'):
            raise ValueError("Phone must start with '+'")
        return v

class NotificationRequest(BaseModel):
    """Схема запроса на отправку уведомления"""
    message: str
    contacts: ContactData
    priority_order: list[str] = ["telegram", "email", "sms"]
    subject: str | None = None

    @field_validator("priority_order")
    def validate_priority(cls, v):
        allowed = {"email", "sms", "telegram"}
        if not set(v).issubset(allowed):
            raise ValueError(f"Invalid channels, allowed: {allowed}")
        return v