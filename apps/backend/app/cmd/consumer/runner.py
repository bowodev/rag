import asyncio
import json

import aio_pika

from app.cmd.consumer.registry import ConsumerSpec
from app.infrastructure.rabbitmq.connection import get_connection


async def run_consumer(spec: ConsumerSpec) -> None:
    connection = await get_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue(spec.queue_name, durable=True)
    print(f"[{spec.name}] waiting on queue: {spec.queue_name}")

    async def _on_message(message: aio_pika.IncomingMessage) -> None:
        async with message.process():
            raw = json.loads(message.body.decode())
            job = spec.model.model_validate(raw)
            await spec.presenter(job)

    await queue.consume(_on_message)
    await asyncio.Future()


async def run_many(specs: list[ConsumerSpec]) -> None:
    await asyncio.gather(*(run_consumer(spec) for spec in specs))