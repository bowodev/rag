from typing import Protocol
from uuid import UUID


class UserRecord(Protocol):
    id: UUID
    email: str
    password_hash: str | None


class IUserRepo(Protocol):
    async def get_by_id(self, user_id: UUID) -> UserRecord | None: ...
    async def get_by_email(self, email: str) -> UserRecord | None: ...


class IUserService(Protocol):
    async def get_by_id(self, *, user_id: UUID) -> UserRecord | None: ...
