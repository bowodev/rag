"""Declare knowledge index queue with dead-letter topology."""

from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from app.config.config import settings


async def declare_knowledge_topology(channel: AbstractChannel) -> None:
    await channel.declare_exchange(
        settings.knowledge_dlx,
        type="direct",
        durable=True,
    )
    dlq = await channel.declare_queue(settings.knowledge_dlq, durable=True)
    await dlq.bind(settings.knowledge_dlx, routing_key=settings.knowledge_dlq)

    await channel.declare_queue(
        settings.knowledge_queue,
        durable=True,
        arguments={
            "x-dead-letter-exchange": settings.knowledge_dlx,
            "x-dead-letter-routing-key": settings.knowledge_dlq,
        },
    )
    await channel.declare_queue(settings.knowledge_recovery_queue, durable=True)


async def ensure_knowledge_topology(connection: AbstractRobustConnection) -> None:
    channel = await connection.channel()
    try:
        await declare_knowledge_topology(channel)
    finally:
        await channel.close()
