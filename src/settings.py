import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", True)
    RABBIT_USER: str = os.getenv("RABBIT_USER", "guest")
    RABBIT_PASS: str = os.getenv("RABBIT_PASS", "guest")
    RABBIT_SERVER: str = os.getenv("RABBIT_SERVER", "localhost:5672")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT: str = os.getenv("SMTP_PORT", "252")
    EMAIL_USER: str = os.getenv("EMAIL_USER", "example@example.com")
    EMAIL_PASS: str = os.getenv("EMAIL_PASS", "password")
    SMS_API_KEY: str = os.getenv("SMS_API_KEY", "apikey")
    SMS_API_URL: str = os.getenv("SMS_API_URL", "https://sms.example.com")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "token")

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}@{self.RABBIT_SERVER}/"


settings = Settings()
