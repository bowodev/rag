from typing import Protocol
from uuid import UUID

from app.application.ports.chunk import ReadyChunkHit


class IChunkEmbeddingRepo(Protocol):
    async def delete_for_source(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> None: ...

    async def upsert_many(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        rows: list[tuple[UUID, list[float]]],
    ) -> list[UUID]: ...

    async def search_ready(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[ReadyChunkHit]: ...
