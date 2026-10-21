from uuid import UUID

from fastapi import status

from app.application.ports.user import IUserService
from app.cmd.api.errors import api_error
from app.domain.auth.context import AuthContext
from app.infrastructure.auth.jwt import decode_access_token
from app.infrastructure.database.enum import PlatformRole


class AuthMiddleware:
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    async def __call__(self, token: str) -> AuthContext:
        if not token:
            raise api_error(
                status.HTTP_401_UNAUTHORIZED,
                message="failed to authenticate",
                error="not authenticated",
            )

        try:
            payload = decode_access_token(token)
            user_id = UUID(payload["sub"])
        except Exception as exc:
            raise api_error(
                status.HTTP_401_UNAUTHORIZED,
                message="failed to authenticate",
                error="invalid token",
            ) from exc

        user = await self._user_service.get_by_id(user_id=user_id)
        if user is None:
            raise api_error(
                status.HTTP_401_UNAUTHORIZED,
                message="failed to authenticate",
                error="invalid token",
            )

        role = getattr(user, "platform_role", PlatformRole.USER)
        role_value = role.value if isinstance(role, PlatformRole) else str(role)

        return AuthContext(
            user_id=user.id,
            email=user.email,
            platform_role=role_value,
        )
