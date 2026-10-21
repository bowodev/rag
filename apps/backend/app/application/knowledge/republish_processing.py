import logging
from datetime import UTC, datetime, timedelta

from app.application.ports.job_bus import JobBus
from app.application.ports.source import ISourceRepo
from app.config.config import settings
from app.domain.dto.jobs import IndexSource

logger = logging.getLogger(__name__)


class RepublishProcessingSources:
    """Re-enqueue IndexSource jobs for stuck processing sources."""

    def __init__(self, sources: ISourceRepo, bus: JobBus) -> None:
        self._sources = sources
        self._bus = bus

    async def __call__(self) -> int:
        older_than = datetime.now(UTC) - timedelta(
            seconds=settings.knowledge_recovery_min_age_seconds
        )
        stuck = await self._sources.list_processing(older_than=older_than)
        published = 0
        for source in stuck:
            await self._bus.publish(
                message=IndexSource(
                    source_id=source.id,
                    tenant_id=source.tenant_id,
                    bot_id=source.bot_id,
                )
            )
            published += 1
        if published:
            logger.info("republished %s stuck processing sources", published)
        return published
