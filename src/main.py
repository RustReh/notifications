import logging
import aio_pika
from pydantic import ValidationError
from src.settings import settings
from src.gateway.gateway import NotificationGateway
from src.schemas.request_schema import NotificationRequest
from src.utils.exceptions import NotificationError

logger = logging.getLogger(__name__)

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            request = NotificationRequest.model_validate_json(message.body)

            gateway = NotificationGateway()

            await gateway.send_with_fallback(request)
            await message.ack()

        except ValidationError as e:
            logger.error(f"Invalid message format: {e.errors()}")
            await message.ack()
        except NotificationError as e:
            logger.error(f"Notification failed: {str(e)}")
            await message.nack(requeue=False)
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
            await message.nack(requeue=True)

async def main():
    """Запуск consumer'а RabbitMQ"""
    connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL,
        client_properties={"connection_name": "notification-service"}
    )

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(
        name="notifications.main",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "notifications.dlx",
            "x-message-ttl": 60000
        }
    )

    await channel.declare_queue(
        name="notifications.dlq",
        durable=True,
        arguments={
            "x-queue-type": "quorum"
        }
    )

    await queue.consume(process_message)
    logger.info("Notification service started consuming messages")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())