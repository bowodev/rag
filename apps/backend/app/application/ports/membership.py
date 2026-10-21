from typing import Protocol
from uuid import UUID


class TenantMembershipRecord(Protocol):
    id: UUID
    name: str
    slug: str
    status: str
    role: str


class IMembershipRepo(Protocol):
    async def list_tenants_for_user(
        self, *, user_id: UUID
    ) -> list[TenantMembershipRecord]: ...

    async def has_membership(self, *, user_id: UUID, tenant_id: UUID) -> bool: ...
