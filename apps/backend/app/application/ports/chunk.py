from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class ChunkPiece:
    ordinal: int
    content: str
    token_count: int | None = None


@dataclass(frozen=True)
class StoredChunk:
    id: UUID
    tenant_id: UUID
    bot_id: UUID
    source_id: UUID
    ordinal: int
    content: str
    vector_id: str | None


@dataclass(frozen=True)
class ReadyChunkHit:
    chunk_id: UUID
    source_id: UUID
    content: str
    ordinal: int
    score: float


class IChunkRepo(Protocol):
    async def delete_for_source(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> None: ...

    async def insert_many(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        source_id: UUID,
        pieces: list[ChunkPiece],
    ) -> list[StoredChunk]: ...

    async def set_vector_id(
        self,
        *,
        chunk_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
        vector_id: str,
    ) -> None: ...
