from typing import Protocol
from uuid import UUID

from app.infrastructure.database.enum import PlatformRole


class UserRecord(Protocol):
    id: UUID
    email: str
    name: str
    password_hash: str | None
    platform_role: PlatformRole


class IUserRepo(Protocol):
    async def get_by_id(self, user_id: UUID) -> UserRecord | None: ...

    async def get_by_email(self, email: str) -> UserRecord | None: ...

    async def list(
        self,
        *,
        q: str | None = None,
        platform_role: PlatformRole | None = None,
    ) -> list[UserRecord]: ...

    async def create(
        self,
        *,
        email: str,
        name: str,
        password_hash: str | None,
        platform_role: PlatformRole,
    ) -> UserRecord: ...

    async def update(
        self,
        user: UserRecord,
        *,
        email: str | None = None,
        name: str | None = None,
        password_hash: str | None = None,
        clear_password: bool = False,
        platform_role: PlatformRole | None = None,
    ) -> UserRecord: ...

    async def delete(self, user: UserRecord) -> None: ...

    async def count_blocking_refs(self, *, user_id: UUID) -> int: ...


class IUserService(Protocol):
    async def get_by_id(self, *, user_id: UUID) -> UserRecord | None: ...
