from uuid import UUID

from app.application.ports.membership import IMembershipRepo
from app.application.ports.tenant import ITenantRepo
from app.application.ports.user import IUserRepo
from app.domain.errors import ConflictError, NotFoundError, ValidationError
from app.domain.membership.detail import MembershipDetail
from app.infrastructure.database.enum import MembershipRole


def _to_detail(m) -> MembershipDetail:  # noqa: ANN001
    role = m.role.value if hasattr(m.role, "value") else str(m.role)
    return MembershipDetail(
        id=m.id,
        tenant_id=m.tenant_id,
        user_id=m.user_id,
        role=role,
        created_at=m.created_at,
    )


class ListMemberships:
    def __init__(self, memberships: IMembershipRepo) -> None:
        self._memberships = memberships

    async def __call__(
        self,
        *,
        tenant_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> list[MembershipDetail]:
        rows = await self._memberships.list(tenant_id=tenant_id, user_id=user_id)
        return [_to_detail(m) for m in rows]


class GetMembership:
    def __init__(self, memberships: IMembershipRepo) -> None:
        self._memberships = memberships

    async def __call__(self, *, membership_id: UUID) -> MembershipDetail:
        membership = await self._memberships.get_by_id(membership_id)
        if membership is None:
            raise NotFoundError("membership not found")
        return _to_detail(membership)


class CreateMembership:
    def __init__(
        self,
        memberships: IMembershipRepo,
        tenants: ITenantRepo,
        users: IUserRepo,
    ) -> None:
        self._memberships = memberships
        self._tenants = tenants
        self._users = users

    async def __call__(
        self,
        *,
        tenant_id: UUID,
        user_id: UUID,
        role: str = MembershipRole.MEMBER.value,
    ) -> MembershipDetail:
        if await self._tenants.get_by_id(tenant_id) is None:
            raise NotFoundError("tenant not found")
        if await self._users.get_by_id(user_id) is None:
            raise NotFoundError("user not found")
        existing = await self._memberships.list(tenant_id=tenant_id, user_id=user_id)
        if existing:
            raise ConflictError("membership already exists")
        try:
            role_enum = MembershipRole(role)
        except ValueError as exc:
            raise ValidationError("invalid role") from exc
        membership = await self._memberships.create(
            tenant_id=tenant_id,
            user_id=user_id,
            role=role_enum,
        )
        return _to_detail(membership)


class UpdateMembership:
    def __init__(self, memberships: IMembershipRepo) -> None:
        self._memberships = memberships

    async def __call__(self, *, membership_id: UUID, role: str) -> MembershipDetail:
        membership = await self._memberships.get_by_id(membership_id)
        if membership is None:
            raise NotFoundError("membership not found")
        try:
            role_enum = MembershipRole(role)
        except ValueError as exc:
            raise ValidationError("invalid role") from exc
        updated = await self._memberships.update_role(membership, role=role_enum)
        return _to_detail(updated)


class DeleteMembership:
    def __init__(self, memberships: IMembershipRepo) -> None:
        self._memberships = memberships

    async def __call__(self, *, membership_id: UUID) -> None:
        membership = await self._memberships.get_by_id(membership_id)
        if membership is None:
            raise NotFoundError("membership not found")
        await self._memberships.delete(membership)
