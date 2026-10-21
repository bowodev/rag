from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from app.application.user.ops_crud import CreateUser, DeleteUser, ListUsers
from app.domain.errors import ConflictError, NotFoundError, ValidationError
from app.infrastructure.database.enum import PlatformRole


@dataclass
class FakeUser:
    id: UUID
    email: str
    name: str
    password_hash: str | None
    platform_role: PlatformRole
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class FakeUserRepo:
    def __init__(self) -> None:
        self.users: dict[UUID, FakeUser] = {}
        self.by_email: dict[str, FakeUser] = {}
        self.blocking = 0

    async def get_by_id(self, user_id: UUID):
        return self.users.get(user_id)

    async def get_by_email(self, email: str):
        return self.by_email.get(email)

    async def list(self, *, q=None, platform_role=None):  # noqa: ANN001
        rows = list(self.users.values())
        if q:
            rows = [u for u in rows if q.lower() in u.email or q.lower() in u.name.lower()]
        if platform_role is not None:
            rows = [u for u in rows if u.platform_role == platform_role]
        return rows

    async def create(self, *, email, name, password_hash, platform_role):  # noqa: ANN001
        user = FakeUser(
            id=uuid4(),
            email=email,
            name=name,
            password_hash=password_hash,
            platform_role=platform_role,
        )
        self.users[user.id] = user
        self.by_email[email] = user
        return user

    async def delete(self, user):  # noqa: ANN001
        self.users.pop(user.id, None)
        self.by_email.pop(user.email, None)

    async def count_blocking_refs(self, *, user_id: UUID) -> int:
        return self.blocking


class FakeMembershipRepo:
    def __init__(self) -> None:
        self.deleted_for: list[UUID] = []

    async def delete_for_user(self, *, user_id: UUID) -> int:
        self.deleted_for.append(user_id)
        return 1


@pytest.mark.asyncio
async def test_create_user_allows_null_password() -> None:
    repo = FakeUserRepo()
    detail = await CreateUser(repo)(
        email="A@Example.com",
        name="Ada",
        password=None,
    )
    assert detail.email == "a@example.com"
    assert detail.has_password is False
    assert detail.platform_role == "user"


@pytest.mark.asyncio
async def test_create_user_rejects_duplicate_email() -> None:
    repo = FakeUserRepo()
    await CreateUser(repo)(email="a@example.com", name="Ada")
    with pytest.raises(ConflictError):
        await CreateUser(repo)(email="a@example.com", name="Other")


@pytest.mark.asyncio
async def test_create_user_requires_fields() -> None:
    with pytest.raises(ValidationError):
        await CreateUser(FakeUserRepo())(email="", name="Ada")


@pytest.mark.asyncio
async def test_list_users_filters_q() -> None:
    repo = FakeUserRepo()
    await CreateUser(repo)(email="ada@example.com", name="Ada")
    await CreateUser(repo)(email="bob@example.com", name="Bob")
    rows = await ListUsers(repo)(q="ada")
    assert len(rows) == 1
    assert rows[0].email == "ada@example.com"


@pytest.mark.asyncio
async def test_delete_user_cascades_memberships() -> None:
    users = FakeUserRepo()
    memberships = FakeMembershipRepo()
    detail = await CreateUser(users)(email="a@example.com", name="Ada")
    await DeleteUser(users, memberships)(user_id=detail.id)
    assert detail.id in memberships.deleted_for
    assert await users.get_by_id(detail.id) is None


@pytest.mark.asyncio
async def test_delete_user_conflict_when_blocking_refs() -> None:
    users = FakeUserRepo()
    users.blocking = 1
    memberships = FakeMembershipRepo()
    detail = await CreateUser(users)(email="a@example.com", name="Ada")
    with pytest.raises(ConflictError):
        await DeleteUser(users, memberships)(user_id=detail.id)


@pytest.mark.asyncio
async def test_delete_user_not_found() -> None:
    with pytest.raises(NotFoundError):
        await DeleteUser(FakeUserRepo(), FakeMembershipRepo())(user_id=uuid4())
