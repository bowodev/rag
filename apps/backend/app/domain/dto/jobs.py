from uuid import UUID

from pydantic import BaseModel


class IndexSource(BaseModel):
    source_id: UUID
    tenant_id: UUID
    bot_id: UUID


class RecoveryTick(BaseModel):
    """Trigger a scan/republish of stuck processing sources."""

    pass
