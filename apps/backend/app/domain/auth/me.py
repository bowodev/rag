from dataclasses import dataclass
from uuid import UUID


@dataclass
class MeResponse:
    user_id: UUID
    email: str
