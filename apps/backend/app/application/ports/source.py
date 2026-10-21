from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.infrastructure.database.enum import SourceStatus


class SourceRecord(Protocol):
    id: UUID
    tenant_id: UUID
    bot_id: UUID
    created_by_user_id: UUID | None
    filename: str
    content_type: str
    byte_size: int | None
    storage_key: str
    status: SourceStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class ISourceRepo(Protocol):
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
    ) -> SourceRecord: ...

    async def get_by_id(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> SourceRecord | None: ...

    async def list_processing(
        self,
        *,
        older_than: datetime | None = None,
        limit: int = 100,
    ) -> list[SourceRecord]: ...

    async def mark_failed(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
        error_message: str,
    ) -> SourceRecord | None: ...

    async def mark_ready(
        self,
        *,
        source_id: UUID,
        tenant_id: UUID,
        bot_id: UUID,
    ) -> SourceRecord | None: ...
