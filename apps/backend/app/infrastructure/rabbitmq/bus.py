import json
from typing import Any

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from pydantic import BaseModel

from app.config.config import settings

def _serialize(message: Any) -> bytes:
    if isinstance(message, BaseModel):
        payload = message.model_dump(mode="json")
    elif isinstance(message, dict):
        payload = message
    else:
        # dataclass / plain object: paksa lewat dict/BaseModel biar aman
        raise TypeError(f"unsupported message type: {type(message)}")
    return json.dumps(payload).encode()

class RabbitMQBus:
    def __init__(
        self,
        connection: AbstractRobustConnection,
        *,
        queue_name: str,
    ) -> None:
        self._connection = connection
        self._queue_name = queue_name
    
    async def publish[T](self, *, message: T) -> None:
        channel = await self._connection.channel()
        try:
            await channel.declare_queue(self._queue_name, durable=True)
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=_serialize(message),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    content_type="application/json",
                ),
                routing_key=self._queue_name,
            )
        finally:
            await channel.close()
