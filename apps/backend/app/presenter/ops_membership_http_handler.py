from uuid import UUID

from app.application.membership.bootstrap import OpsMembershipService
from app.domain.membership.detail import MembershipDetail
from app.presenter.ops_http_errors import map_ops_errors


class OpsMembershipHTTPHandler:
    def __init__(self, service: OpsMembershipService) -> None:
        self._service = service

    async def list(
        self,
        *,
        tenant_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> list[MembershipDetail]:
        return await map_ops_errors(
            message="failed to list memberships",
            call=lambda: self._service.list(tenant_id=tenant_id, user_id=user_id),
        )

    async def get(self, *, membership_id: UUID) -> MembershipDetail:
        return await map_ops_errors(
            message="failed to get membership",
            call=lambda: self._service.get(membership_id=membership_id),
        )

    async def create(
        self,
        *,
        tenant_id: UUID,
        user_id: UUID,
        role: str = "member",
    ) -> MembershipDetail:
        return await map_ops_errors(
            message="failed to create membership",
            call=lambda: self._service.create(
                tenant_id=tenant_id, user_id=user_id, role=role
            ),
        )

    async def update(self, *, membership_id: UUID, role: str) -> MembershipDetail:
        return await map_ops_errors(
            message="failed to update membership",
            call=lambda: self._service.update(membership_id=membership_id, role=role),
        )

    async def delete(self, *, membership_id: UUID) -> None:
        await map_ops_errors(
            message="failed to delete membership",
            call=lambda: self._service.delete(membership_id=membership_id),
        )
