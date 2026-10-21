from typing import Protocol
from uuid import UUID


class BotRecord(Protocol):
    id: UUID
    tenant_id: UUID
    name: str
    status: object


class IBotRepo(Protocol):
    async def get_by_id(self, *, bot_id: UUID) -> BotRecord | None: ...
