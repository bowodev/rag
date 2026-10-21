import logging

from app.application.ports.source import ISourceRepo
from app.domain.dto.jobs import IndexSource

logger = logging.getLogger(__name__)


class MarkSourceFailedFromDlq:
    def __init__(self, sources: ISourceRepo) -> None:
        self._sources = sources

    async def __call__(self, job: IndexSource, *, error_message: str) -> None:
        updated = await self._sources.mark_failed(
            source_id=job.source_id,
            tenant_id=job.tenant_id,
            bot_id=job.bot_id,
            error_message=error_message,
        )
        if updated is None:
            logger.warning(
                "dlq source not found source_id=%s tenant_id=%s bot_id=%s",
                job.source_id,
                job.tenant_id,
                job.bot_id,
            )
        else:
            logger.info("source marked failed from dlq source_id=%s", job.source_id)
