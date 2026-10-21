from dataclasses import dataclass
from uuid import uuid4

import pytest

from app.application.auth.password_helper import hash_password, verify_password
from app.application.auth.set_password import SetPassword
from app.domain.errors import ConflictError, ValidationError


@dataclass
class FakeUser:
    id: object
    email: str
    name: str = "A"
    password_hash: str | None = None
    platform_role: str = "user"
    created_at: object = None
    updated_at: object = None


class FakeUserRepo:
    def __init__(self, user: FakeUser | None) -> None:
        self._user = user

    async def get_by_email(self, email: str):
        if self._user and self._user.email == email:
            return self._user
        return None

    async def update(self, user, **kwargs):  # noqa: ANN001
        if kwargs.get("password_hash") is not None:
            user.password_hash = kwargs["password_hash"]
        return user


@pytest.mark.asyncio
async def test_set_password_success_when_null() -> None:
    user = FakeUser(id=uuid4(), email="a@example.com", password_hash=None)
    await SetPassword(FakeUserRepo(user))(email="a@example.com", password="secret12")
    assert user.password_hash is not None
    assert verify_password("secret12", user.password_hash)


@pytest.mark.asyncio
async def test_set_password_conflict_when_already_set() -> None:
    user = FakeUser(
        id=uuid4(),
        email="a@example.com",
        password_hash=hash_password("oldpass12"),
    )
    with pytest.raises(ConflictError, match="password cannot be set"):
        await SetPassword(FakeUserRepo(user))(email="a@example.com", password="secret12")


@pytest.mark.asyncio
async def test_set_password_conflict_when_missing_user() -> None:
    with pytest.raises(ConflictError, match="password cannot be set"):
        await SetPassword(FakeUserRepo(None))(email="missing@example.com", password="secret12")


@pytest.mark.asyncio
async def test_set_password_validation() -> None:
    uc = SetPassword(FakeUserRepo(None))
    with pytest.raises(ValidationError):
        await uc(email="", password="secret12")
    with pytest.raises(ValidationError):
        await uc(email="a@example.com", password="short")
