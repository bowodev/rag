import logging
from pathlib import PurePosixPath
from uuid import UUID, uuid4

from app.application.knowledge.validate_upload import storage_key, validate_upload
from app.application.ports.bot import IBotRepo
from app.application.ports.job_bus import JobBus
from app.application.ports.membership import IMembershipRepo
from app.application.ports.object_storage import ObjectStorage
from app.application.ports.source import ISourceRepo, SourceRecord
from app.domain.dto.jobs import IndexSource
from app.domain.errors import ForbiddenError
from app.domain.knowledge.source import SourceDetail
from app.infrastructure.database.enum import SourceStatus

logger = logging.getLogger(__name__)


def _to_detail(source: SourceRecord) -> SourceDetail:
    status = source.status
    status_value = status.value if hasattr(status, "value") else str(status)
    return SourceDetail(
        id=source.id,
        tenant_id=source.tenant_id,
        bot_id=source.bot_id,
        filename=source.filename,
        content_type=source.content_type,
        byte_size=source.byte_size,
        status=status_value,
        error_message=source.error_message,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )


class UploadSource:
    def __init__(
        self,
        bots: IBotRepo,
        memberships: IMembershipRepo,
        sources: ISourceRepo,
        storage: ObjectStorage,
        bus: JobBus,
    ) -> None:
        self._bots = bots
        self._memberships = memberships
        self._sources = sources
        self._storage = storage
        self._bus = bus

    async def __call__(
        self,
        *,
        user_id: UUID,
        bot_id: UUID,
        filename: str,
        content_type: str,
        data: bytes,
    ) -> SourceDetail:
        bot = await self._bots.get_by_id(bot_id=bot_id)
        if bot is None:
            raise ForbiddenError("bot access denied")

        allowed = await self._memberships.has_membership(
            user_id=user_id,
            tenant_id=bot.tenant_id,
        )
        if not allowed:
            raise ForbiddenError("bot access denied")

        canonical_type = validate_upload(
            filename=filename,
            content_type=content_type,
            byte_size=len(data),
        )

        source_id = uuid4()
        key = storage_key(
            tenant_id=str(bot.tenant_id),
            bot_id=str(bot_id),
            source_id=str(source_id),
            filename=filename,
        )
        await self._storage.put(key=key, body=data, content_type=canonical_type)

        source = await self._sources.create(
            id=source_id,
            tenant_id=bot.tenant_id,
            bot_id=bot_id,
            created_by_user_id=user_id,
            filename=PurePosixPath(filename).name,
            content_type=canonical_type,
            byte_size=len(data),
            storage_key=key,
            status=SourceStatus.PROCESSING,
        )

        try:
            await self._bus.publish(
                message=IndexSource(
                    source_id=source.id,
                    tenant_id=bot.tenant_id,
                    bot_id=bot_id,
                )
            )
        except Exception:
            logger.exception(
                "enqueue failed; source left processing source_id=%s",
                source.id,
            )

        return _to_detail(source)
