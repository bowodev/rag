from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserDetail:
    id: UUID
    email: str
    name: str
    platform_role: str
    has_password: bool
    created_at: datetime
    updated_at: datetime
