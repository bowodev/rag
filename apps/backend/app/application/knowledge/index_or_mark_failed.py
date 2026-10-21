import logging
from collections.abc import Awaitable, Callable

from app.application.knowledge.index_source import IndexUploadedSource
from app.application.ports.source import ISourceRepo
from app.domain.dto.jobs import IndexSource

logger = logging.getLogger(__name__)

_MAX_ERROR_LEN = 2000


class IndexOrMarkFailed:
    """Run indexing; on any error optionally recover then mark Source failed (no re-raise)."""

    def __init__(
        self,
        index: IndexUploadedSource,
        sources: ISourceRepo,
        *,
        before_mark_failed: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        self._index = index
        self._sources = sources
        self._before_mark_failed = before_mark_failed

    async def __call__(self, job: IndexSource) -> None:
        try:
            await self._index(job)
        except Exception as exc:
            message = str(exc)[:_MAX_ERROR_LEN] or exc.__class__.__name__
            logger.exception(
                "indexing failed source_id=%s: %s",
                job.source_id,
                message,
            )
            if self._before_mark_failed is not None:
                await self._before_mark_failed()
            try:
                await self._sources.mark_failed(
                    source_id=job.source_id,
                    tenant_id=job.tenant_id,
                    bot_id=job.bot_id,
                    error_message=message,
                )
            except Exception:
                logger.exception(
                    "mark_failed also failed source_id=%s",
                    job.source_id,
                )
