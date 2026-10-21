from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.knowledge.mark_failed import MarkSourceFailedFromDlq
from app.application.knowledge.republish_processing import RepublishProcessingSources
from app.domain.dto.jobs import IndexSource
from app.infrastructure.database.enum import SourceStatus


@dataclass
class FakeSource:
    id: object
    tenant_id: object
    bot_id: object
    status: SourceStatus
    error_message: str | None = None
    updated_at: datetime | None = None


class FakeSourceRepo:
    def __init__(self, sources: list[FakeSource] | None = None) -> None:
        self.sources = sources or []
        self.failed: list[tuple[object, str]] = []

    async def list_processing(self, *, older_than=None, limit: int = 100):  # noqa: ANN001
        rows = [s for s in self.sources if s.status == SourceStatus.PROCESSING]
        if older_than is not None:
            rows = [s for s in rows if s.updated_at and s.updated_at <= older_than]
        return rows[:limit]

    async def mark_failed(
        self,
        *,
        source_id,
        tenant_id,
        bot_id,
        error_message: str,
    ):  # noqa: ANN001
        for s in self.sources:
            if s.id == source_id and s.tenant_id == tenant_id and s.bot_id == bot_id:
                s.status = SourceStatus.FAILED
                s.error_message = error_message
                self.failed.append((source_id, error_message))
                return s
        return None


class FakeBus:
    def __init__(self) -> None:
        self.messages: list[object] = []

    async def publish(self, *, message):  # noqa: ANN001
        self.messages.append(message)


@pytest.mark.asyncio
async def test_mark_failed_from_dlq() -> None:
    source_id = uuid4()
    tenant_id = uuid4()
    bot_id = uuid4()
    repo = FakeSourceRepo(
        [
            FakeSource(
                id=source_id,
                tenant_id=tenant_id,
                bot_id=bot_id,
                status=SourceStatus.PROCESSING,
            )
        ]
    )
    await MarkSourceFailedFromDlq(repo)(
        IndexSource(source_id=source_id, tenant_id=tenant_id, bot_id=bot_id),
        error_message="indexing dead-lettered",
    )
    assert repo.sources[0].status == SourceStatus.FAILED
    assert repo.sources[0].error_message == "indexing dead-lettered"


@pytest.mark.asyncio
async def test_republish_processing_publishes_jobs() -> None:
    source_id = uuid4()
    tenant_id = uuid4()
    bot_id = uuid4()
    old = datetime(2020, 1, 1, tzinfo=UTC)
    repo = FakeSourceRepo(
        [
            FakeSource(
                id=source_id,
                tenant_id=tenant_id,
                bot_id=bot_id,
                status=SourceStatus.PROCESSING,
                updated_at=old,
            )
        ]
    )
    bus = FakeBus()
    count = await RepublishProcessingSources(repo, bus)()
    assert count == 1
    assert isinstance(bus.messages[0], IndexSource)
    assert bus.messages[0].source_id == source_id
