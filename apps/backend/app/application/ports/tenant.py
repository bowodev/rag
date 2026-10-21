from typing import Protocol
from uuid import UUID

from app.infrastructure.database.enum import TenantStatus


class TenantRecord(Protocol):
    id: UUID
    name: str
    slug: str
    status: TenantStatus


class ITenantRepo(Protocol):
    async def get_by_id(self, tenant_id: UUID) -> TenantRecord | None: ...

    async def get_by_slug(self, slug: str) -> TenantRecord | None: ...

    async def list(
        self,
        *,
        q: str | None = None,
        status: TenantStatus | None = None,
    ) -> list[TenantRecord]: ...

    async def create(
        self,
        *,
        name: str,
        slug: str,
        status: TenantStatus,
    ) -> TenantRecord: ...

    async def update(
        self,
        tenant: TenantRecord,
        *,
        name: str | None = None,
        slug: str | None = None,
        status: TenantStatus | None = None,
    ) -> TenantRecord: ...

    async def delete(self, tenant: TenantRecord) -> None: ...

    async def count_bots(self, *, tenant_id: UUID) -> int: ...
