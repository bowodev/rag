from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from app.config.config import settings
from app.domain.dto.jobs import IndexSource, RecoveryTick
from app.presenter.knowledge_event_handler import (
    knowledge_dlq_handler,
    knowledge_recovery_handler,
)
from app.presenter.test_event_handler import test_event_handler


Presenter = Callable[[Any], Awaitable[None]]


@dataclass(frozen=True)
class ConsumerSpec:
    name: str
    queue_name: str
    model: type[BaseModel]
    presenter: Presenter
    poll_interval_seconds: float | None = None
    declare_knowledge_topology: bool = False


CONSUMERS: dict[str, ConsumerSpec] = {
    "test": ConsumerSpec(
        name="test",
        queue_name="test",
        model=IndexSource,
        presenter=test_event_handler,
    ),
    "knowledge-dlq": ConsumerSpec(
        name="knowledge-dlq",
        queue_name=settings.knowledge_dlq,
        model=IndexSource,
        presenter=knowledge_dlq_handler,
        declare_knowledge_topology=True,
    ),
    "knowledge-recovery": ConsumerSpec(
        name="knowledge-recovery",
        queue_name=settings.knowledge_recovery_queue,
        model=RecoveryTick,
        presenter=knowledge_recovery_handler,
        poll_interval_seconds=settings.knowledge_recovery_interval_seconds,
        declare_knowledge_topology=True,
    ),
}


def get_consumer(name: str) -> ConsumerSpec:
    try:
        return CONSUMERS[name]
    except KeyError as exc:
        known = ", ".join(sorted(CONSUMERS))
        raise SystemExit(f"unknown consumer '{name}'. known: {known}") from exc
