from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.chunk import ChunkPiece, IChunkRepo, StoredChunk
from app.infrastructure.database.model.chunk import Chunk


class ChunkRepository(IChunkRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def delete_for_source(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> None:
        await self._session.execute(
            delete(Chunk).where(
                Chunk.source_id == source_id,
                Chunk.tenant_id == tenant_id,
                Chunk.bot_id == bot_id,
            )
        )

    async def insert_many(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        source_id: UUID,
        pieces: list[ChunkPiece],
    ) -> list[StoredChunk]:
        rows: list[Chunk] = []
        for piece in pieces:
            row = Chunk(
                tenant_id=tenant_id,
                bot_id=bot_id,
                source_id=source_id,
                ordinal=piece.ordinal,
                content=piece.content,
                token_count=piece.token_count,
                vector_id=None,
                chunk_metadata={},
            )
            self._session.add(row)
            rows.append(row)
        await self._session.flush()
        return [
            StoredChunk(
                id=row.id,
                tenant_id=row.tenant_id,
                bot_id=row.bot_id,
                source_id=row.source_id,
                ordinal=row.ordinal,
                content=row.content,
                vector_id=row.vector_id,
            )
            for row in rows
        ]

    async def set_vector_id(
        self,
        *,
        chunk_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
        vector_id: str,
    ) -> None:
        await self._session.execute(
            update(Chunk)
            .where(
                Chunk.id == chunk_id,
                Chunk.tenant_id == tenant_id,
                Chunk.bot_id == bot_id,
            )
            .values(vector_id=vector_id)
        )
