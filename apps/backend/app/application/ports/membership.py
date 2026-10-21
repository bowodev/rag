from typing import Protocol
from uuid import UUID

from app.infrastructure.database.enum import MembershipRole


class TenantMembershipRecord(Protocol):
    id: UUID
    name: str
    slug: str
    status: str
    role: str


class MembershipRecord(Protocol):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    role: MembershipRole


class IMembershipRepo(Protocol):
    async def list_tenants_for_user(
        self, *, user_id: UUID
    ) -> list[TenantMembershipRecord]: ...

    async def has_membership(self, *, user_id: UUID, tenant_id: UUID) -> bool: ...

    async def get_by_id(self, membership_id: UUID) -> MembershipRecord | None: ...

    async def list(
        self,
        *,
        tenant_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> list[MembershipRecord]: ...

    async def create(
        self,
        *,
        tenant_id: UUID,
        user_id: UUID,
        role: MembershipRole,
    ) -> MembershipRecord: ...

    async def update_role(
        self,
        membership: MembershipRecord,
        *,
        role: MembershipRole,
    ) -> MembershipRecord: ...

    async def delete(self, membership: MembershipRecord) -> None: ...

    async def delete_for_user(self, *, user_id: UUID) -> int: ...

    async def delete_for_tenant(self, *, tenant_id: UUID) -> int: ...
