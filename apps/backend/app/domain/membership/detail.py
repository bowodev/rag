from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class MembershipDetail:
    id: UUID
    tenant_id: UUID
    user_id: UUID
    role: str
    created_at: datetime
