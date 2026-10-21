from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class BotSummary:
    id: UUID
    name: str
    status: str
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime
