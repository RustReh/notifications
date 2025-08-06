import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", True)
    RABBIT_USER: str = os.getenv("RABBIT_USER", "guest")
    RABBIT_PASS: str = os.getenv("RABBIT_PASS", "guest")
    RABBIT_SERVER: str = os.getenv("RABBIT_SERVER", "localhost:5672")

    @property
    def RABBITMQ_URL(self):
        return (f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}@{self.RABBIT_SERVER}/",)
