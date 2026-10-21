from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.knowledge.upload_source import UploadSource
from app.domain.dto.jobs import IndexSource
from app.domain.errors import ForbiddenError, ValidationError
from app.infrastructure.database.enum import SourceStatus


@dataclass
class FakeBot:
    id: object
    tenant_id: object
    name: str = "bot"
    status: str = "live"


@dataclass
class FakeSource:
    id: object
    tenant_id: object
    bot_id: object
    created_by_user_id: object
    filename: str
    content_type: str
    byte_size: int | None
    storage_key: str
    status: SourceStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class FakeBotRepo:
    def __init__(self, bot: FakeBot | None) -> None:
        self._bot = bot

    async def get_by_id(self, *, bot_id):  # noqa: ANN001
        if self._bot is None or self._bot.id != bot_id:
            return None
        return self._bot


class FakeMembershipRepo:
    def __init__(self, *, allowed: bool) -> None:
        self._allowed = allowed

    async def has_membership(self, *, user_id, tenant_id) -> bool:  # noqa: ANN001
        return self._allowed


class FakeSourceRepo:
    def __init__(self) -> None:
        self.created: list[FakeSource] = []

    async def create(self, **kwargs):  # noqa: ANN003
        now = datetime.now(UTC)
        source = FakeSource(
            error_message=None,
            created_at=now,
            updated_at=now,
            **kwargs,
        )
        self.created.append(source)
        return source


class FakeStorage:
    def __init__(self) -> None:
        self.puts: list[tuple[str, bytes, str]] = []

    async def ensure_bucket(self) -> None:
        return None

    async def put(self, *, key: str, body: bytes, content_type: str) -> None:
        self.puts.append((key, body, content_type))

    async def delete(self, *, key: str) -> None:
        return None


class FakeBus:
    def __init__(self, *, fail: bool = False) -> None:
        self.fail = fail
        self.messages: list[object] = []

    async def publish(self, *, message):  # noqa: ANN001
        if self.fail:
            raise RuntimeError("broker down")
        self.messages.append(message)


@pytest.mark.asyncio
async def test_upload_happy_path_enqueues() -> None:
    tenant_id = uuid4()
    bot_id = uuid4()
    user_id = uuid4()
    bots = FakeBotRepo(FakeBot(id=bot_id, tenant_id=tenant_id))
    sources = FakeSourceRepo()
    storage = FakeStorage()
    bus = FakeBus()

    detail = await UploadSource(
        bots, FakeMembershipRepo(allowed=True), sources, storage, bus
    )(
        user_id=user_id,
        bot_id=bot_id,
        filename="notes.pdf",
        content_type="application/pdf",
        data=b"%PDF-1.4",
    )

    assert detail.status == "processing"
    assert detail.filename == "notes.pdf"
    assert len(storage.puts) == 1
    assert len(sources.created) == 1
    assert len(bus.messages) == 1
    assert isinstance(bus.messages[0], IndexSource)
    assert bus.messages[0].bot_id == bot_id


@pytest.mark.asyncio
async def test_upload_forbidden_without_membership() -> None:
    bot_id = uuid4()
    bots = FakeBotRepo(FakeBot(id=bot_id, tenant_id=uuid4()))
    with pytest.raises(ForbiddenError):
        await UploadSource(
            bots,
            FakeMembershipRepo(allowed=False),
            FakeSourceRepo(),
            FakeStorage(),
            FakeBus(),
        )(
            user_id=uuid4(),
            bot_id=bot_id,
            filename="notes.pdf",
            content_type="application/pdf",
            data=b"%PDF",
        )


@pytest.mark.asyncio
async def test_upload_forbidden_missing_bot() -> None:
    with pytest.raises(ForbiddenError):
        await UploadSource(
            FakeBotRepo(None),
            FakeMembershipRepo(allowed=True),
            FakeSourceRepo(),
            FakeStorage(),
            FakeBus(),
        )(
            user_id=uuid4(),
            bot_id=uuid4(),
            filename="notes.pdf",
            content_type="application/pdf",
            data=b"%PDF",
        )


@pytest.mark.asyncio
async def test_upload_rejects_bad_type() -> None:
    bot_id = uuid4()
    bots = FakeBotRepo(FakeBot(id=bot_id, tenant_id=uuid4()))
    with pytest.raises(ValidationError):
        await UploadSource(
            bots,
            FakeMembershipRepo(allowed=True),
            FakeSourceRepo(),
            FakeStorage(),
            FakeBus(),
        )(
            user_id=uuid4(),
            bot_id=bot_id,
            filename="malware.exe",
            content_type="application/octet-stream",
            data=b"x",
        )


@pytest.mark.asyncio
async def test_upload_publish_failure_still_returns_processing() -> None:
    tenant_id = uuid4()
    bot_id = uuid4()
    bots = FakeBotRepo(FakeBot(id=bot_id, tenant_id=tenant_id))
    sources = FakeSourceRepo()
    bus = FakeBus(fail=True)

    detail = await UploadSource(
        bots, FakeMembershipRepo(allowed=True), sources, FakeStorage(), bus
    )(
        user_id=uuid4(),
        bot_id=bot_id,
        filename="notes.txt",
        content_type="text/plain",
        data=b"hello",
    )

    assert detail.status == "processing"
    assert len(sources.created) == 1
    assert bus.messages == []
