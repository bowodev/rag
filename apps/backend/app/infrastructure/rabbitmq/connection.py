import aio_pika
from aio_pika.abc import AbstractRobustConnection

from app.config.config import settings


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)