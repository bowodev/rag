from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SourceDetail:
    id: UUID
    tenant_id: UUID
    bot_id: UUID
    filename: str
    content_type: str
    byte_size: int | None
    status: str
    error_message: str | None
    created_at: datetime
    updated_at: datetime
