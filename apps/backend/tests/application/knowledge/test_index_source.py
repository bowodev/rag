from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from app.application.knowledge.index_or_mark_failed import IndexOrMarkFailed
from app.application.knowledge.index_source import IndexUploadedSource
from app.application.ports.chunk import StoredChunk
from app.domain.dto.jobs import IndexSource
from app.infrastructure.database.enum import SourceStatus


@dataclass
class FakeSource:
    id: UUID
    tenant_id: UUID
    bot_id: UUID
    filename: str
    content_type: str
    storage_key: str
    status: SourceStatus
    error_message: str | None = None
    created_by_user_id: UUID | None = None
    byte_size: int | None = 10
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class FakeSourceRepo:
    def __init__(self, source: FakeSource | None) -> None:
        self.source = source
        self.failed: list[tuple[UUID, str]] = []
        self.ready: list[UUID] = []

    async def get_by_id(self, *, source_id, tenant_id, bot_id):  # noqa: ANN001
        if (
            self.source is None
            or self.source.id != source_id
            or self.source.tenant_id != tenant_id
            or self.source.bot_id != bot_id
        ):
            return None
        return self.source

    async def mark_failed(self, *, source_id, tenant_id, bot_id, error_message):  # noqa: ANN001
        assert self.source is not None
        self.source.status = SourceStatus.FAILED
        self.source.error_message = error_message
        self.failed.append((source_id, error_message))
        return self.source

    async def mark_ready(self, *, source_id, tenant_id, bot_id):  # noqa: ANN001
        assert self.source is not None
        self.source.status = SourceStatus.READY
        self.source.error_message = None
        self.ready.append(source_id)
        return self.source


class FakeStorage:
    def __init__(self, objects: dict[str, bytes] | None = None) -> None:
        self.objects = objects or {}

    async def get(self, *, key: str) -> bytes:
        return self.objects[key]


class FakeExtractor:
    def __init__(self, text: str = "hello world about bots") -> None:
        self.text = text
        self.calls = 0

    def extract(self, *, body: bytes, content_type: str, filename: str) -> str:
        self.calls += 1
        if self.text == "__raise__":
            raise ValueError("extract boom")
        return self.text


class FakeEmbedder:
    def __init__(self, *, fail: bool = False, dim: int = 8) -> None:
        self.fail = fail
        self.dim = dim
        self.calls: list[list[str]] = []

    async def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(texts)
        if self.fail:
            raise RuntimeError("embed boom")
        return [[float(i + 1)] * self.dim for i, _ in enumerate(texts)]


class FakeChunkRepo:
    def __init__(self) -> None:
        self.deleted: list[UUID] = []
        self.inserted: list[StoredChunk] = []
        self.vector_ids: dict[UUID, str] = {}

    async def delete_for_source(self, *, source_id, tenant_id, bot_id) -> None:  # noqa: ANN001
        self.deleted.append(source_id)
        self.inserted = [c for c in self.inserted if c.source_id != source_id]

    async def insert_many(self, *, tenant_id, bot_id, source_id, pieces):  # noqa: ANN001
        rows = [
            StoredChunk(
                id=uuid4(),
                tenant_id=tenant_id,
                bot_id=bot_id,
                source_id=source_id,
                ordinal=p.ordinal,
                content=p.content,
                vector_id=None,
            )
            for p in pieces
        ]
        self.inserted.extend(rows)
        return rows

    async def set_vector_id(self, *, chunk_id, tenant_id, bot_id, vector_id):  # noqa: ANN001
        self.vector_ids[chunk_id] = vector_id


class FakeEmbeddingRepo:
    def __init__(self) -> None:
        self.deleted: list[UUID] = []
        self.rows: list[tuple[UUID, UUID, UUID, list[float]]] = []

    async def delete_for_source(self, *, source_id, tenant_id, bot_id) -> None:  # noqa: ANN001
        self.deleted.append(source_id)
        self.rows.clear()

    async def upsert_many(self, *, tenant_id, bot_id, rows):  # noqa: ANN001
        ids: list[UUID] = []
        for chunk_id, vector in rows:
            eid = uuid4()
            ids.append(eid)
            self.rows.append((chunk_id, tenant_id, bot_id, vector))
        return ids

def _job_and_source(**kwargs):  # noqa: ANN003
    tenant_id = uuid4()
    bot_id = uuid4()
    source_id = uuid4()
    source = FakeSource(
        id=source_id,
        tenant_id=tenant_id,
        bot_id=bot_id,
        filename="a.txt",
        content_type="text/plain",
        storage_key="t/b/s/a.txt",
        status=SourceStatus.PROCESSING,
        **kwargs,
    )
    job = IndexSource(source_id=source_id, tenant_id=tenant_id, bot_id=bot_id)
    return job, source


@pytest.mark.asyncio
async def test_index_success_marks_ready_and_upserts() -> None:
    job, source = _job_and_source()
    sources = FakeSourceRepo(source)
    chunks = FakeChunkRepo()
    embeddings = FakeEmbeddingRepo()
    await IndexUploadedSource(
        sources,
        FakeStorage({source.storage_key: b"hello"}),
        chunks,
        embeddings,
        FakeExtractor("enough text to index"),
        FakeEmbedder(),
    )(job)
    assert source.status == SourceStatus.READY
    assert sources.ready == [source.id]
    assert chunks.deleted == [source.id]
    assert embeddings.deleted == [source.id]
    assert len(chunks.inserted) >= 1
    assert len(embeddings.rows) == len(chunks.inserted)
    assert all(cid in chunks.vector_ids for cid in (c.id for c in chunks.inserted))
    assert all(
        row[1] == source.tenant_id and row[2] == source.bot_id
        for row in embeddings.rows
    )


@pytest.mark.asyncio
async def test_index_idempotent_replaces_prior_chunks() -> None:
    job, source = _job_and_source()
    chunks = FakeChunkRepo()
    embeddings = FakeEmbeddingRepo()
    uc = IndexUploadedSource(
        FakeSourceRepo(source),
        FakeStorage({source.storage_key: b"hello"}),
        chunks,
        embeddings,
        FakeExtractor("first pass text"),
        FakeEmbedder(),
    )
    await uc(job)
    first_ids = {c.id for c in chunks.inserted}
    source.status = SourceStatus.PROCESSING
    await uc(job)
    assert chunks.deleted == [source.id, source.id]
    assert {c.id for c in chunks.inserted}.isdisjoint(first_ids)


@pytest.mark.asyncio
async def test_index_or_mark_failed_on_extract_error() -> None:
    job, source = _job_and_source()
    sources = FakeSourceRepo(source)
    await IndexOrMarkFailed(
        IndexUploadedSource(
            sources,
            FakeStorage({source.storage_key: b"x"}),
            FakeChunkRepo(),
            FakeEmbeddingRepo(),
            FakeExtractor("__raise__"),
            FakeEmbedder(),
        ),
        sources,
    )(job)
    assert source.status == SourceStatus.FAILED
    assert "extract boom" in (source.error_message or "")


@pytest.mark.asyncio
async def test_index_or_mark_failed_on_embed_error() -> None:
    job, source = _job_and_source()
    sources = FakeSourceRepo(source)
    await IndexOrMarkFailed(
        IndexUploadedSource(
            sources,
            FakeStorage({source.storage_key: b"x"}),
            FakeChunkRepo(),
            FakeEmbeddingRepo(),
            FakeExtractor("ok text"),
            FakeEmbedder(fail=True),
        ),
        sources,
    )(job)
    assert source.status == SourceStatus.FAILED
    assert "embed boom" in (source.error_message or "")


@pytest.mark.asyncio
async def test_index_skips_non_processing() -> None:
    job, source = _job_and_source()
    source.status = SourceStatus.READY
    extractor = FakeExtractor()
    await IndexUploadedSource(
        FakeSourceRepo(source),
        FakeStorage({source.storage_key: b"x"}),
        FakeChunkRepo(),
        FakeEmbeddingRepo(),
        extractor,
        FakeEmbedder(),
    )(job)
    assert extractor.calls == 0
