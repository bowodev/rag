from typing import Annotated
from uuid import UUID

from app.application.user.bootstrap import UserService
from app.cmd.api.errors import api_error
from app.domain.auth.context import AuthContext
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.repository.user import UserRepository
from app.infrastructure.database.session import get_session
from app.middleware.auth import AuthMiddleware
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

bearer = HTTPBearer(auto_error=False)


async def require_auth(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthContext:
    token = ""
    if creds is not None and creds.scheme.lower() == "bearer":
        token = creds.credentials

    auth = AuthMiddleware(
        user_service=UserService(user_repo=UserRepository(session)),
    )
    return await auth(token)


async def require_tenant_membership(
    tenant_id: UUID,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthContext:
    """Fail closed unless the caller has an active membership for tenant_id."""
    memberships = MembershipRepository(session)
    allowed = await memberships.has_membership(
        user_id=ctx.user_id,
        tenant_id=tenant_id,
    )
    if not allowed:
        raise api_error(
            status.HTTP_403_FORBIDDEN,
            message="failed to authorize",
            error="tenant access denied",
        )
    return ctx
