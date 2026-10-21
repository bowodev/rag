from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TenantSummary:
    id: UUID
    name: str
    slug: str
    status: str
    role: str
