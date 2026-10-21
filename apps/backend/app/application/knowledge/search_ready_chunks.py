from uuid import UUID

from app.application.ports.chunk import ReadyChunkHit
from app.application.ports.chunk_embedding import IChunkEmbeddingRepo


class SearchReadyChunks:
    def __init__(self, embeddings: IChunkEmbeddingRepo) -> None:
        self._embeddings = embeddings

    async def __call__(
        self,
        *,
        tenant_id: UUID,
        bot_id: UUID,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[ReadyChunkHit]:
        return await self._embeddings.search_ready(
            tenant_id=tenant_id,
            bot_id=bot_id,
            query_embedding=query_embedding,
            limit=limit,
        )
