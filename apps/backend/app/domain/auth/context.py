from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AuthContext:
    user_id: UUID
    email: str
    platform_role: str  # "user" | "ops"
