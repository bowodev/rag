from app.application.auth.password_helper import hash_password
from app.application.ports.user import IUserRepo
from app.domain.errors import ConflictError, ValidationError

_CANNOT_SET = "password cannot be set"


class SetPassword:
    def __init__(self, user_repo: IUserRepo) -> None:
        self._user_repo = user_repo

    async def __call__(self, *, email: str, password: str) -> None:
        if not email:
            raise ValidationError("Email is required")
        if not password:
            raise ValidationError("Password is required")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        user = await self._user_repo.get_by_email(email)
        # Stable messaging: missing user and already-set hash look the same.
        if user is None or user.password_hash is not None:
            raise ConflictError(_CANNOT_SET)

        await self._user_repo.update(user, password_hash=hash_password(password))
