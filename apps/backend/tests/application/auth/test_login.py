from dataclasses import dataclass
from uuid import uuid4

import pytest

from app.application.auth.login import Login
from app.application.auth.password_helper import hash_password
from app.domain.errors import UnauthorizedError, ValidationError


@dataclass
class FakeUser:
    id: object
    email: str
    password_hash: str | None


class FakeUserRepo:
    def __init__(self, user: FakeUser | None) -> None:
        self._user = user

    async def get_by_id(self, user_id):  # noqa: ANN001
        if self._user and self._user.id == user_id:
            return self._user
        return None

    async def get_by_email(self, email: str):
        if self._user and self._user.email == email:
            return self._user
        return None


@pytest.mark.asyncio
async def test_login_success_uses_password_hash() -> None:
    user = FakeUser(
        id=uuid4(),
        email="a@example.com",
        password_hash=hash_password("secret"),
    )
    result = await Login(FakeUserRepo(user))(email="a@example.com", password="secret")
    assert result.email == "a@example.com"
    assert result.token_type == "Bearer"
    assert result.access_token
    assert result.refresh_token


@pytest.mark.asyncio
async def test_login_unknown_email_is_generic() -> None:
    with pytest.raises(UnauthorizedError, match="invalid credentials"):
        await Login(FakeUserRepo(None))(email="missing@example.com", password="x")


@pytest.mark.asyncio
async def test_login_wrong_password_is_generic() -> None:
    user = FakeUser(
        id=uuid4(),
        email="a@example.com",
        password_hash=hash_password("secret"),
    )
    with pytest.raises(UnauthorizedError, match="invalid credentials"):
        await Login(FakeUserRepo(user))(email="a@example.com", password="nope")


@pytest.mark.asyncio
async def test_login_null_password_hash_is_generic() -> None:
    user = FakeUser(id=uuid4(), email="a@example.com", password_hash=None)
    with pytest.raises(UnauthorizedError, match="invalid credentials"):
        await Login(FakeUserRepo(user))(email="a@example.com", password="secret")


@pytest.mark.asyncio
async def test_login_requires_email_and_password() -> None:
    login = Login(FakeUserRepo(None))
    with pytest.raises(ValidationError):
        await login(email="", password="x")
    with pytest.raises(ValidationError):
        await login(email="a@example.com", password="")
