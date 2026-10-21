import inspect
from uuid import uuid4

import pytest

from app.application.knowledge.search_ready_chunks import SearchReadyChunks
from app.application.ports.chunk import ReadyChunkHit
from app.infrastructure.database.enum import SourceStatus
from app.infrastructure.database.repository.chunk_embedding import (
    ChunkEmbeddingRepository,
)


class FakeEmbeddingRepo:
    def __init__(self) -> None:
        self._hits: list[tuple[SourceStatus, ReadyChunkHit]] = []

    def seed(self, status: SourceStatus, hit: ReadyChunkHit) -> None:
        self._hits.append((status, hit))

    async def search_ready(self, *, tenant_id, bot_id, query_embedding, limit=5):  # noqa: ANN001
        # Mirrors ChunkEmbeddingRepository contract: only READY sources.
        return [
            hit for status, hit in self._hits if status == SourceStatus.READY
        ][:limit]


@pytest.mark.asyncio
async def test_search_ready_excludes_processing_and_failed() -> None:
    repo = FakeEmbeddingRepo()
    ready_id = uuid4()
    processing_id = uuid4()
    failed_id = uuid4()
    repo.seed(
        SourceStatus.READY,
        ReadyChunkHit(
            chunk_id=ready_id,
            source_id=uuid4(),
            content="ready chunk",
            ordinal=0,
            score=0.9,
        ),
    )
    repo.seed(
        SourceStatus.PROCESSING,
        ReadyChunkHit(
            chunk_id=processing_id,
            source_id=uuid4(),
            content="processing chunk",
            ordinal=0,
            score=0.95,
        ),
    )
    repo.seed(
        SourceStatus.FAILED,
        ReadyChunkHit(
            chunk_id=failed_id,
            source_id=uuid4(),
            content="failed chunk",
            ordinal=0,
            score=0.99,
        ),
    )

    hits = await SearchReadyChunks(repo)(
        tenant_id=uuid4(),
        bot_id=uuid4(),
        query_embedding=[0.1, 0.2],
        limit=10,
    )
    assert [h.chunk_id for h in hits] == [ready_id]
    assert all(h.content == "ready chunk" for h in hits)


def test_chunk_embedding_repo_search_ready_filters_status() -> None:
    source = inspect.getsource(ChunkEmbeddingRepository.search_ready)
    assert "SourceStatus.READY" in source
