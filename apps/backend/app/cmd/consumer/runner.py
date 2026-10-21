import asyncio
import json
import logging

import aio_pika

from app.cmd.consumer.registry import ConsumerSpec
from app.infrastructure.rabbitmq.connection import get_connection
from app.infrastructure.rabbitmq.topology import declare_knowledge_topology

logger = logging.getLogger(__name__)


async def run_consumer(spec: ConsumerSpec) -> None:
    connection = await get_connection()
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    if spec.declare_knowledge_topology:
        await declare_knowledge_topology(channel)
        # Queue already declared with full args; passive avoid inequivalent-arg errors.
        queue = await channel.declare_queue(
            spec.queue_name,
            durable=True,
            passive=True,
        )
    else:
        queue = await channel.declare_queue(spec.queue_name, durable=True)
    print(f"[{spec.name}] waiting on queue: {spec.queue_name}")

    async def _on_message(message: aio_pika.IncomingMessage) -> None:
        async with message.process(requeue=False):
            raw = json.loads(message.body.decode())
            job = spec.model.model_validate(raw)
            await spec.presenter(job)

    await queue.consume(_on_message)

    if spec.poll_interval_seconds is not None and spec.poll_interval_seconds > 0:

        async def _poll_loop() -> None:
            while True:
                try:
                    tick = spec.model.model_validate({})
                    await spec.presenter(tick)
                except Exception:
                    logger.exception("[%s] poll tick failed", spec.name)
                await asyncio.sleep(spec.poll_interval_seconds)

        asyncio.create_task(_poll_loop())
        print(
            f"[{spec.name}] poll interval: {spec.poll_interval_seconds}s",
        )

    await asyncio.Future()


async def run_many(specs: list[ConsumerSpec]) -> None:
    await asyncio.gather(*(run_consumer(spec) for spec in specs))
