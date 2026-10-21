from collections.abc import Sequence
from datetime import datetime
from typing import Protocol
from uuid import UUID


class BotRecord(Protocol):
    id: UUID
    tenant_id: UUID
    name: str
    status: object
    created_at: datetime
    updated_at: datetime


class IBotRepo(Protocol):
    async def get_by_id(self, *, bot_id: UUID) -> BotRecord | None: ...

    async def list_by_tenant_ids(
        self, *, tenant_ids: Sequence[UUID]
    ) -> list[BotRecord]: ...
