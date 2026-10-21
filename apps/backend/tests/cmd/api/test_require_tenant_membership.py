from dataclasses import dataclass
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.cmd.api.deps.auth import require_tenant_membership
from app.domain.auth.context import AuthContext


@dataclass
class FakeRepo:
    allowed: bool

    async def has_membership(self, *, user_id, tenant_id) -> bool:  # noqa: ANN001
        return self.allowed


@pytest.mark.asyncio
async def test_require_tenant_membership_denies_without_membership() -> None:
    ctx = AuthContext(user_id=uuid4(), email="a@example.com", platform_role="user")
    with patch(
        "app.cmd.api.deps.auth.MembershipRepository",
        return_value=FakeRepo(allowed=False),
    ):
        with pytest.raises(HTTPException) as exc:
            await require_tenant_membership(
                tenant_id=uuid4(),
                ctx=ctx,
                session=object(),  # type: ignore[arg-type]
            )
        assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_require_tenant_membership_allows_member() -> None:
    ctx = AuthContext(user_id=uuid4(), email="a@example.com", platform_role="user")
    with patch(
        "app.cmd.api.deps.auth.MembershipRepository",
        return_value=FakeRepo(allowed=True),
    ):
        result = await require_tenant_membership(
            tenant_id=uuid4(),
            ctx=ctx,
            session=object(),  # type: ignore[arg-type]
        )
        assert result is ctx
