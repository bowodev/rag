from uuid import UUID

from app.application.user.bootstrap import OpsUserService
from app.domain.user.detail import UserDetail
from app.presenter.ops_http_errors import map_ops_errors


class OpsUserHTTPHandler:
    def __init__(self, service: OpsUserService) -> None:
        self._service = service

    async def list(
        self, *, q: str | None = None, platform_role: str | None = None
    ) -> list[UserDetail]:
        return await map_ops_errors(
            message="failed to list users",
            call=lambda: self._service.list(q=q, platform_role=platform_role),
        )

    async def get(self, *, user_id: UUID) -> UserDetail:
        return await map_ops_errors(
            message="failed to get user",
            call=lambda: self._service.get(user_id=user_id),
        )

    async def create(
        self,
        *,
        email: str,
        name: str,
        password: str | None = None,
        platform_role: str = "user",
    ) -> UserDetail:
        return await map_ops_errors(
            message="failed to create user",
            call=lambda: self._service.create(
                email=email,
                name=name,
                password=password,
                platform_role=platform_role,
            ),
        )

    async def update(
        self,
        *,
        user_id: UUID,
        email: str | None = None,
        name: str | None = None,
        password: str | None = None,
        platform_role: str | None = None,
    ) -> UserDetail:
        return await map_ops_errors(
            message="failed to update user",
            call=lambda: self._service.update(
                user_id=user_id,
                email=email,
                name=name,
                password=password,
                platform_role=platform_role,
            ),
        )

    async def delete(self, *, user_id: UUID) -> None:
        await map_ops_errors(
            message="failed to delete user",
            call=lambda: self._service.delete(user_id=user_id),
        )
