from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.bot.get_for_user import GetBotForUser
from app.application.bot.list_for_user import ListBotsForUser
from app.domain.errors import ForbiddenError


@dataclass
class FakeTenant:
    id: object
    name: str = "t"
    slug: str = "t"
    status: str = "active"
    role: str = "member"


@dataclass
class FakeBot:
    id: object
    tenant_id: object
    name: str
    status: object
    created_at: datetime
    updated_at: datetime


class FakeBotRepo:
    def __init__(self, bots: list[FakeBot]) -> None:
        self._bots = bots
        self.listed_tenant_ids: list[object] | None = None

    async def get_by_id(self, *, bot_id):  # noqa: ANN001
        for bot in self._bots:
            if bot.id == bot_id:
                return bot
        return None

    async def list_by_tenant_ids(self, *, tenant_ids):  # noqa: ANN001
        self.listed_tenant_ids = list(tenant_ids)
        allowed = set(tenant_ids)
        return [bot for bot in self._bots if bot.tenant_id in allowed]


class FakeMembershipRepo:
    def __init__(
        self,
        *,
        tenants: list[FakeTenant] | None = None,
        allowed_pairs: set[tuple[object, object]] | None = None,
    ) -> None:
        self._tenants = tenants or []
        self._allowed_pairs = allowed_pairs or set()

    async def list_tenants_for_user(self, *, user_id):  # noqa: ANN001
        return list(self._tenants)

    async def has_membership(self, *, user_id, tenant_id) -> bool:  # noqa: ANN001
        return (user_id, tenant_id) in self._allowed_pairs


def _bot(
    *,
    tenant_id: object,
    name: str = "bot",
    status: str = "live",
) -> FakeBot:
    now = datetime.now(UTC)
    return FakeBot(
        id=uuid4(),
        tenant_id=tenant_id,
        name=name,
        status=status,
        created_at=now,
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_list_empty_memberships_returns_empty() -> None:
    uc = ListBotsForUser(FakeBotRepo([_bot(tenant_id=uuid4())]), FakeMembershipRepo())
    assert await uc(user_id=uuid4()) == []


@pytest.mark.asyncio
async def test_list_scopes_to_membership_tenants_all_statuses() -> None:
    tenant_a = uuid4()
    tenant_b = uuid4()
    other = uuid4()
    bots = [
        _bot(tenant_id=tenant_a, name="a-draft", status="draft"),
        _bot(tenant_id=tenant_a, name="a-live", status="live"),
        _bot(tenant_id=tenant_b, name="b-disabled", status="disabled"),
        _bot(tenant_id=other, name="other", status="live"),
    ]
    repo = FakeBotRepo(bots)
    uc = ListBotsForUser(
        repo,
        FakeMembershipRepo(
            tenants=[FakeTenant(id=tenant_a), FakeTenant(id=tenant_b, name="b", slug="b")],
        ),
    )

    result = await uc(user_id=uuid4())

    assert repo.listed_tenant_ids == [tenant_a, tenant_b]
    assert {row.name for row in result} == {"a-draft", "a-live", "b-disabled"}
    assert {row.status for row in result} == {"draft", "live", "disabled"}
    for row in result:
        assert hasattr(row, "created_at")
        assert hasattr(row, "updated_at")
        assert not hasattr(row, "prompt")
        assert not hasattr(row, "model")
        assert not hasattr(row, "temperature")


@pytest.mark.asyncio
async def test_get_happy_path() -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    bot = _bot(tenant_id=tenant_id, name="alpha", status="draft")
    uc = GetBotForUser(
        FakeBotRepo([bot]),
        FakeMembershipRepo(allowed_pairs={(user_id, tenant_id)}),
    )

    result = await uc(user_id=user_id, bot_id=bot.id)

    assert result.id == bot.id
    assert result.name == "alpha"
    assert result.status == "draft"
    assert result.tenant_id == tenant_id


@pytest.mark.asyncio
async def test_get_missing_bot_forbidden() -> None:
    uc = GetBotForUser(FakeBotRepo([]), FakeMembershipRepo())
    with pytest.raises(ForbiddenError, match="bot access denied"):
        await uc(user_id=uuid4(), bot_id=uuid4())


@pytest.mark.asyncio
async def test_get_cross_tenant_forbidden() -> None:
    user_id = uuid4()
    bot = _bot(tenant_id=uuid4())
    uc = GetBotForUser(
        FakeBotRepo([bot]),
        FakeMembershipRepo(allowed_pairs=set()),
    )
    with pytest.raises(ForbiddenError, match="bot access denied"):
        await uc(user_id=user_id, bot_id=bot.id)
