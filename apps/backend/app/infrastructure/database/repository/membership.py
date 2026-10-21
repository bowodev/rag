from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.membership import IMembershipRepo
from app.infrastructure.database.enum import TenantStatus
from app.infrastructure.database.model.membership import Membership
from app.infrastructure.database.model.tenant import Tenant


@dataclass(frozen=True)
class TenantMembershipRow:
    id: UUID
    name: str
    slug: str
    status: str
    role: str


class MembershipRepository(IMembershipRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_tenants_for_user(self, *, user_id: UUID) -> list[TenantMembershipRow]:
        stmt = (
            select(
                Tenant.id,
                Tenant.name,
                Tenant.slug,
                Tenant.status,
                Membership.role,
            )
            .join(Membership, Membership.tenant_id == Tenant.id)
            .where(
                Membership.user_id == user_id,
                Tenant.status == TenantStatus.ACTIVE,
            )
            .order_by(Tenant.name)
        )
        result = await self._session.execute(stmt)
        return [
            TenantMembershipRow(
                id=row.id,
                name=row.name,
                slug=row.slug,
                status=row.status.value if hasattr(row.status, "value") else str(row.status),
                role=row.role.value if hasattr(row.role, "value") else str(row.role),
            )
            for row in result.all()
        ]

    async def has_membership(self, *, user_id: UUID, tenant_id: UUID) -> bool:
        stmt = (
            select(Membership.id)
            .join(Tenant, Tenant.id == Membership.tenant_id)
            .where(
                Membership.user_id == user_id,
                Membership.tenant_id == tenant_id,
                Tenant.status == TenantStatus.ACTIVE,
            )
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
