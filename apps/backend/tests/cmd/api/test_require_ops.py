from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.cmd.api.deps.auth import require_ops
from app.domain.auth.context import AuthContext


@pytest.mark.asyncio
async def test_require_ops_denies_user_role() -> None:
    ctx = AuthContext(user_id=uuid4(), email="a@example.com", platform_role="user")
    with pytest.raises(HTTPException) as exc:
        await require_ops(ctx=ctx)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_require_ops_allows_ops_role() -> None:
    ctx = AuthContext(user_id=uuid4(), email="ops@example.com", platform_role="ops")
    assert await require_ops(ctx=ctx) is ctx
