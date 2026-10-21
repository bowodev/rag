from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class TenantDetail:
    id: UUID
    name: str
    slug: str
    status: str
    created_at: datetime
    updated_at: datetime
