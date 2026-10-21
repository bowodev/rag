from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from app.domain.dto.jobs import IndexSource
from app.presenter.test_event_handler import test_event_handler


Presenter = Callable[[Any], Awaitable[None]]


@dataclass(frozen=True)
class ConsumerSpec:
    name: str
    queue_name: str
    model: type[BaseModel]
    presenter: Presenter


CONSUMERS: dict[str, ConsumerSpec] = {
    "test": ConsumerSpec(
        name="test",
        queue_name="test",  # samakan dengan API publish; nanti settings.knowledge_queue
        model=IndexSource,
        presenter=test_event_handler,
    ),
}


def get_consumer(name: str) -> ConsumerSpec:
    try:
        return CONSUMERS[name]
    except KeyError as exc:
        known = ", ".join(sorted(CONSUMERS))
        raise SystemExit(f"unknown consumer '{name}'. known: {known}") from exc