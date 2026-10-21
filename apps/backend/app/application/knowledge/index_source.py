import logging

from app.application.ports.chunk import IChunkRepo
from app.application.ports.chunk_embedding import IChunkEmbeddingRepo
from app.application.ports.embedder import Embedder
from app.application.ports.object_storage import ObjectStorage
from app.application.ports.source import ISourceRepo
from app.application.ports.text_extractor import TextExtractor
from app.config.config import settings
from app.domain.dto.jobs import IndexSource
from app.infrastructure.database.enum import SourceStatus
from app.infrastructure.knowledge.chunker import chunk_text

logger = logging.getLogger(__name__)


class IndexUploadedSource:
    """Extract → chunk → embed → upsert; raises on failure (presenter marks failed)."""

    def __init__(
        self,
        sources: ISourceRepo,
        storage: ObjectStorage,
        chunks: IChunkRepo,
        embeddings: IChunkEmbeddingRepo,
        extractor: TextExtractor,
        embedder: Embedder,
    ) -> None:
        self._sources = sources
        self._storage = storage
        self._chunks = chunks
        self._embeddings = embeddings
        self._extractor = extractor
        self._embedder = embedder

    async def __call__(self, job: IndexSource) -> None:
        source = await self._sources.get_by_id(
            source_id=job.source_id,
            tenant_id=job.tenant_id,
            bot_id=job.bot_id,
        )
        if source is None:
            logger.warning(
                "index skip: source not found source_id=%s",
                job.source_id,
            )
            return
        if source.status != SourceStatus.PROCESSING:
            logger.info(
                "index skip: status=%s source_id=%s",
                source.status,
                job.source_id,
            )
            return

        body = await self._storage.get(key=source.storage_key)
        text = self._extractor.extract(
            body=body,
            content_type=source.content_type,
            filename=source.filename,
        )
        pieces = chunk_text(
            text,
            size=settings.chunk_size_chars,
            overlap=settings.chunk_overlap_chars,
        )
        if not pieces:
            raise ValueError("no chunks produced from source text")

        vectors = await self._embedder.embed([p.content for p in pieces])
        if len(vectors) != len(pieces):
            raise ValueError(
                f"embedder returned {len(vectors)} vectors for {len(pieces)} chunks"
            )

        await self._embeddings.delete_for_source(
            source_id=source.id,
            tenant_id=source.tenant_id,
            bot_id=source.bot_id,
        )
        await self._chunks.delete_for_source(
            source_id=source.id,
            tenant_id=source.tenant_id,
            bot_id=source.bot_id,
        )

        stored = await self._chunks.insert_many(
            tenant_id=source.tenant_id,
            bot_id=source.bot_id,
            source_id=source.id,
            pieces=pieces,
        )
        embedding_ids = await self._embeddings.upsert_many(
            tenant_id=source.tenant_id,
            bot_id=source.bot_id,
            rows=[(chunk.id, vectors[i]) for i, chunk in enumerate(stored)],
        )
        for chunk, embedding_id in zip(stored, embedding_ids, strict=True):
            await self._chunks.set_vector_id(
                chunk_id=chunk.id,
                tenant_id=source.tenant_id,
                bot_id=source.bot_id,
                vector_id=str(embedding_id),
            )

        await self._sources.mark_ready(
            source_id=source.id,
            tenant_id=source.tenant_id,
            bot_id=source.bot_id,
        )
        logger.info(
            "indexed source_id=%s chunks=%s",
            source.id,
            len(stored),
        )
