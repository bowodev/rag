from uuid import UUID

from app.application.ports.membership import IMembershipRepo
from app.domain.tenant.summary import TenantSummary


class ListTenantsForUser:
    def __init__(self, memberships: IMembershipRepo) -> None:
        self._memberships = memberships

    async def __call__(self, *, user_id: UUID) -> list[TenantSummary]:
        rows = await self._memberships.list_tenants_for_user(user_id=user_id)
        return [
            TenantSummary(
                id=row.id,
                name=row.name,
                slug=row.slug,
                status=row.status,
                role=row.role,
            )
            for row in rows
        ]
