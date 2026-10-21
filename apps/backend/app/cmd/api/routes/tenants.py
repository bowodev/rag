from typing import Annotated

from app.application.tenant.bootstrap import TenantService
from app.cmd.api.deps.auth import require_auth
from app.domain.auth.context import AuthContext
from app.domain.tenant.summary import TenantSummary
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.session import get_session
from app.presenter.tenant_http_handler import TenantHTTPHandler
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/tenants",
    tags=["tenants"],
    dependencies=[Depends(require_auth)],
)


async def get_tenant_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TenantHTTPHandler:
    return TenantHTTPHandler(
        tenant_service=TenantService(
            membership_repo=MembershipRepository(session),
        ),
    )


@router.get("", response_model=list[TenantSummary])
async def list_tenants(
    ctx: Annotated[AuthContext, Depends(require_auth)],
    handler: Annotated[TenantHTTPHandler, Depends(get_tenant_handler)],
):
    return await handler.list_for_user(user_id=ctx.user_id)
