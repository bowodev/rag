from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.source import ISourceRepo
from app.infrastructure.database.enum import SourceStatus
from app.infrastructure.database.model.source import Source


class SourceRepository(ISourceRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
        created_by_user_id: UUID | None,
        filename: str,
        content_type: str,
        byte_size: int | None,
        storage_key: str,
        status: SourceStatus = SourceStatus.PROCESSING,
    ) -> Source:
        source = Source(
            id=id,
            tenant_id=tenant_id,
            bot_id=bot_id,
            created_by_user_id=created_by_user_id,
            filename=filename,
            content_type=content_type,
            byte_size=byte_size,
            storage_key=storage_key,
            status=status,
        )
        self._session.add(source)
        await self._session.flush()
        return source

    async def get_by_id(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> Source | None:
        stmt = select(Source).where(
            Source.id == source_id,
            Source.tenant_id == tenant_id,
            Source.bot_id == bot_id,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_processing(
        self,
        *,
        older_than: datetime | None = None,
        limit: int = 100,
    ) -> list[Source]:
        stmt = select(Source).where(Source.status == SourceStatus.PROCESSING)
        if older_than is not None:
            stmt = stmt.where(Source.updated_at <= older_than)
        stmt = stmt.order_by(Source.updated_at.asc()).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def mark_failed(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
        error_message: str,
    ) -> Source | None:
        source = await self.get_by_id(
            source_id=source_id,
            tenant_id=tenant_id,
            bot_id=bot_id,
        )
        if source is None:
            return None
        source.status = SourceStatus.FAILED
        source.error_message = error_message
        await self._session.flush()
        return source

    async def mark_ready(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> Source | None:
        source = await self.get_by_id(
            source_id=source_id,
            tenant_id=tenant_id,
            bot_id=bot_id,
        )
        if source is None:
            return None
        source.status = SourceStatus.READY
        source.error_message = None
        await self._session.flush()
        return source
