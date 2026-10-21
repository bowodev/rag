from typing import Annotated

from app.cmd.api.deps.auth import require_auth
from app.domain.auth.context import AuthContext
from fastapi import APIRouter, Depends

router = APIRouter(tags=["auth"])


@router.get("/me")
async def me(ctx: Annotated[AuthContext, Depends(require_auth)]):
    return {"user_id": str(ctx.user_id), "email": ctx.email}
