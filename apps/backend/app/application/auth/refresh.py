from uuid import UUID

from app.application.ports.user import IUserRepo
from app.config.config import settings
from app.domain.auth.login import LoginResponse
from app.domain.errors import UnauthorizedError, ValidationError
from app.infrastructure.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

_INVALID_TOKEN = "invalid token"


class Refresh:
    def __init__(self, user_repo: IUserRepo) -> None:
        self._user_repo = user_repo

    async def __call__(self, *, refresh_token: str) -> LoginResponse:
        if not refresh_token:
            raise ValidationError("Refresh token is required")

        try:
            payload = decode_refresh_token(refresh_token)
            user_id = UUID(payload["sub"])
        except (ValueError, KeyError, TypeError) as exc:
            raise UnauthorizedError(_INVALID_TOKEN) from exc

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UnauthorizedError(_INVALID_TOKEN)

        return LoginResponse(
            access_token=create_access_token(user_id=user.id),
            refresh_token=create_refresh_token(user_id=user.id),
            token_type="Bearer",
            expires_in=settings.jwt_ttl_seconds,
            user_id=user.id,
            email=user.email,
        )
