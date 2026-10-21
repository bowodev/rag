from dataclasses import dataclass
from uuid import uuid4

import pytest

from app.application.auth.refresh import Refresh
from app.domain.errors import UnauthorizedError, ValidationError
from app.infrastructure.auth.jwt import create_access_token, create_refresh_token


@dataclass
class FakeUser:
    id: object
    email: str
    password_hash: str | None = "x"


class FakeUserRepo:
    def __init__(self, user: FakeUser | None) -> None:
        self._user = user

    async def get_by_id(self, user_id):  # noqa: ANN001
        if self._user and self._user.id == user_id:
            return self._user
        return None

    async def get_by_email(self, email: str):
        return None


@pytest.mark.asyncio
async def test_refresh_issues_new_tokens() -> None:
    user = FakeUser(id=uuid4(), email="a@example.com")
    token = create_refresh_token(user_id=user.id)
    result = await Refresh(FakeUserRepo(user))(refresh_token=token)
    assert result.user_id == user.id
    assert result.access_token
    assert result.refresh_token


@pytest.mark.asyncio
async def test_refresh_rejects_access_token() -> None:
    user = FakeUser(id=uuid4(), email="a@example.com")
    access = create_access_token(user_id=user.id)
    with pytest.raises(UnauthorizedError, match="invalid token"):
        await Refresh(FakeUserRepo(user))(refresh_token=access)


@pytest.mark.asyncio
async def test_refresh_rejects_unknown_user() -> None:
    token = create_refresh_token(user_id=uuid4())
    with pytest.raises(UnauthorizedError, match="invalid token"):
        await Refresh(FakeUserRepo(None))(refresh_token=token)


@pytest.mark.asyncio
async def test_refresh_requires_token() -> None:
    with pytest.raises(ValidationError):
        await Refresh(FakeUserRepo(None))(refresh_token="")
