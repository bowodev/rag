import logging

from app.application.knowledge.index_or_mark_failed import IndexOrMarkFailed
from app.application.knowledge.index_source import IndexUploadedSource
from app.application.knowledge.mark_failed import MarkSourceFailedFromDlq
from app.application.knowledge.republish_processing import RepublishProcessingSources
from app.config.config import settings
from app.domain.dto.jobs import IndexSource, RecoveryTick
from app.infrastructure.database.repository.chunk import ChunkRepository
from app.infrastructure.database.repository.chunk_embedding import (
    ChunkEmbeddingRepository,
)
from app.infrastructure.database.repository.source import SourceRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.knowledge.extract import FileTextExtractor
from app.infrastructure.knowledge.openai_embedder import OpenAIEmbedder
from app.infrastructure.rabbitmq.bus import RabbitMQBus
from app.infrastructure.rabbitmq.connection import get_connection
from app.infrastructure.storage.s3 import S3ObjectStorage

logger = logging.getLogger(__name__)


async def knowledge_index_handler(job: IndexSource) -> None:
    async with SessionLocal() as session:
        sources = SourceRepository(session)
        await IndexOrMarkFailed(
            IndexUploadedSource(
                sources,
                S3ObjectStorage(),
                ChunkRepository(session),
                ChunkEmbeddingRepository(session),
                FileTextExtractor(),
                OpenAIEmbedder(),
            ),
            sources,
            before_mark_failed=session.rollback,
        )(job)
        await session.commit()


async def knowledge_dlq_handler(job: IndexSource) -> None:
    async with SessionLocal() as session:
        await MarkSourceFailedFromDlq(SourceRepository(session))(
            job,
            error_message="indexing dead-lettered",
        )
        await session.commit()


async def knowledge_recovery_handler(_tick: RecoveryTick) -> None:
    connection = await get_connection()
    try:
        bus = RabbitMQBus(connection, queue_name=settings.knowledge_queue)
        async with SessionLocal() as session:
            await RepublishProcessingSources(SourceRepository(session), bus)()
            await session.commit()
    finally:
        await connection.close()
