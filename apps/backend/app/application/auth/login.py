from app.application.auth.password_helper import verify_password
from app.application.ports.user import IUserRepo
from app.config.config import settings
from app.domain.auth.login import LoginResponse
from app.domain.errors import UnauthorizedError, ValidationError
from app.infrastructure.auth.jwt import create_access_token, create_refresh_token

_INVALID_CREDENTIALS = "invalid credentials"


class Login:
    def __init__(self, user_repo: IUserRepo) -> None:
        self._user_repo = user_repo

    async def __call__(self, *, email: str, password: str) -> LoginResponse:
        self._validate(email, password)

        user = await self._user_repo.get_by_email(email)
        if user is None or not user.password_hash:
            raise UnauthorizedError(_INVALID_CREDENTIALS)

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError(_INVALID_CREDENTIALS)

        return LoginResponse(
            access_token=create_access_token(user_id=user.id),
            refresh_token=create_refresh_token(user_id=user.id),
            token_type="Bearer",
            expires_in=settings.jwt_ttl_seconds,
            user_id=user.id,
            email=user.email,
        )

    def _validate(self, email: str, password: str) -> None:
        if not email:
            raise ValidationError("Email is required")
        if not password:
            raise ValidationError("Password is required")
