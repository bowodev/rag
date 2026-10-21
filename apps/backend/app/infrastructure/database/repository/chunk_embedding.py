from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.chunk import ReadyChunkHit
from app.application.ports.chunk_embedding import IChunkEmbeddingRepo
from app.infrastructure.database.enum import SourceStatus
from app.infrastructure.database.model.chunk import Chunk
from app.infrastructure.database.model.chunk_embedding import ChunkEmbedding
from app.infrastructure.database.model.source import Source


class ChunkEmbeddingRepository(IChunkEmbeddingRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def delete_for_source(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> None:
        chunk_ids = select(Chunk.id).where(
            Chunk.source_id == source_id,
            Chunk.tenant_id == tenant_id,
            Chunk.bot_id == bot_id,
        )
        await self._session.execute(
            delete(ChunkEmbedding).where(ChunkEmbedding.chunk_id.in_(chunk_ids))
        )

    async def upsert_many(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        rows: list[tuple[UUID, list[float]]],
    ) -> list[UUID]:
        created: list[ChunkEmbedding] = []
        for chunk_id, vector in rows:
            row = ChunkEmbedding(
                chunk_id=chunk_id,
                tenant_id=tenant_id,
                bot_id=bot_id,
                embedding=vector,
            )
            self._session.add(row)
            created.append(row)
        await self._session.flush()
        return [row.id for row in created]

    async def search_ready(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[ReadyChunkHit]:
        distance = ChunkEmbedding.embedding.cosine_distance(query_embedding)
        stmt = (
            select(
                Chunk.id,
                Chunk.source_id,
                Chunk.content,
                Chunk.ordinal,
                distance.label("distance"),
            )
            .join(ChunkEmbedding, ChunkEmbedding.chunk_id == Chunk.id)
            .join(Source, Source.id == Chunk.source_id)
            .where(
                Chunk.tenant_id == tenant_id,
                Chunk.bot_id == bot_id,
                ChunkEmbedding.tenant_id == tenant_id,
                ChunkEmbedding.bot_id == bot_id,
                Source.status == SourceStatus.READY,
            )
            .order_by(distance)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        hits: list[ReadyChunkHit] = []
        for chunk_id, source_id, content, ordinal, dist in result.all():
            score = 1.0 / (1.0 + float(dist))
            hits.append(
                ReadyChunkHit(
                    chunk_id=chunk_id,
                    source_id=source_id,
                    content=content,
                    ordinal=ordinal,
                    score=score,
                )
            )
        return hits
