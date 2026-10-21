from uuid import UUID

from app.application.auth.password_helper import hash_password
from app.application.ports.membership import IMembershipRepo
from app.application.ports.user import IUserRepo
from app.domain.errors import ConflictError, NotFoundError, ValidationError
from app.domain.user.detail import UserDetail
from app.infrastructure.database.enum import PlatformRole


def _to_detail(user) -> UserDetail:  # noqa: ANN001
    role = user.platform_role
    role_value = role.value if hasattr(role, "value") else str(role)
    return UserDetail(
        id=user.id,
        email=user.email,
        name=user.name,
        platform_role=role_value,
        has_password=user.password_hash is not None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class ListUsers:
    def __init__(self, users: IUserRepo) -> None:
        self._users = users

    async def __call__(
        self,
        *,
        q: str | None = None,
        platform_role: str | None = None,
    ) -> list[UserDetail]:
        role = None
        if platform_role:
            try:
                role = PlatformRole(platform_role)
            except ValueError as exc:
                raise ValidationError("invalid platform_role") from exc
        rows = await self._users.list(q=q, platform_role=role)
        return [_to_detail(u) for u in rows]


class GetUser:
    def __init__(self, users: IUserRepo) -> None:
        self._users = users

    async def __call__(self, *, user_id: UUID) -> UserDetail:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise NotFoundError("user not found")
        return _to_detail(user)


class CreateUser:
    def __init__(self, users: IUserRepo) -> None:
        self._users = users

    async def __call__(
        self,
        *,
        email: str,
        name: str,
        password: str | None = None,
        platform_role: str = PlatformRole.USER.value,
    ) -> UserDetail:
        email = email.strip().lower()
        name = name.strip()
        if not email:
            raise ValidationError("email is required")
        if not name:
            raise ValidationError("name is required")
        if password is not None and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        existing = await self._users.get_by_email(email)
        if existing is not None:
            raise ConflictError("email already exists")
        try:
            role = PlatformRole(platform_role)
        except ValueError as exc:
            raise ValidationError("invalid platform_role") from exc
        password_hash = hash_password(password) if password else None
        user = await self._users.create(
            email=email,
            name=name,
            password_hash=password_hash,
            platform_role=role,
        )
        return _to_detail(user)


class UpdateUser:
    def __init__(self, users: IUserRepo) -> None:
        self._users = users

    async def __call__(
        self,
        *,
        user_id: UUID,
        email: str | None = None,
        name: str | None = None,
        password: str | None = None,
        platform_role: str | None = None,
    ) -> UserDetail:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise NotFoundError("user not found")
        if email is not None:
            email = email.strip().lower()
            if not email:
                raise ValidationError("email is required")
            other = await self._users.get_by_email(email)
            if other is not None and other.id != user_id:
                raise ConflictError("email already exists")
        if name is not None and not name.strip():
            raise ValidationError("name is required")
        if password is not None and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        role = None
        if platform_role is not None:
            try:
                role = PlatformRole(platform_role)
            except ValueError as exc:
                raise ValidationError("invalid platform_role") from exc
        updated = await self._users.update(
            user,
            email=email,
            name=name.strip() if name is not None else None,
            password_hash=hash_password(password) if password is not None else None,
            platform_role=role,
        )
        return _to_detail(updated)


class DeleteUser:
    def __init__(self, users: IUserRepo, memberships: IMembershipRepo) -> None:
        self._users = users
        self._memberships = memberships

    async def __call__(self, *, user_id: UUID) -> None:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise NotFoundError("user not found")
        if await self._users.count_blocking_refs(user_id=user_id) > 0:
            raise ConflictError("user has dependent resources")
        await self._memberships.delete_for_user(user_id=user_id)
        await self._users.delete(user)
