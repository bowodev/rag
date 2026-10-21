from typing import Annotated
from uuid import UUID

from pydantic import BaseModel

from app.application.tenant.bootstrap import OpsTenantService
from app.cmd.api.deps.auth import require_ops
from app.domain.auth.context import AuthContext
from app.domain.tenant.detail import TenantDetail
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.repository.tenant import TenantRepository
from app.infrastructure.database.session import get_session
from app.presenter.ops_tenant_http_handler import OpsTenantHTTPHandler
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/tenants",
    tags=["internal-tenants"],
    dependencies=[Depends(require_ops)],
)


class CreateTenantBody(BaseModel):
    name: str
    slug: str
    status: str = "active"


class UpdateTenantBody(BaseModel):
    name: str | None = None
    slug: str | None = None
    status: str | None = None


async def get_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OpsTenantHTTPHandler:
    return OpsTenantHTTPHandler(
        OpsTenantService(
            tenant_repo=TenantRepository(session),
            membership_repo=MembershipRepository(session),
        )
    )


@router.get("", response_model=list[TenantDetail])
async def list_tenants(
    handler: Annotated[OpsTenantHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
    q: Annotated[str | None, Query()] = None,
    status_filter: Annotated[str | None, Query(alias="status")] = None,
):
    return await handler.list(q=q, status=status_filter)


@router.post("", response_model=TenantDetail, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    body: CreateTenantBody,
    handler: Annotated[OpsTenantHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.create(name=body.name, slug=body.slug, status=body.status)


@router.get("/{tenant_id}", response_model=TenantDetail)
async def get_tenant(
    tenant_id: UUID,
    handler: Annotated[OpsTenantHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.get(tenant_id=tenant_id)


@router.patch("/{tenant_id}", response_model=TenantDetail)
async def update_tenant(
    tenant_id: UUID,
    body: UpdateTenantBody,
    handler: Annotated[OpsTenantHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.update(
        tenant_id=tenant_id,
        name=body.name,
        slug=body.slug,
        status=body.status,
    )


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: UUID,
    handler: Annotated[OpsTenantHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    await handler.delete(tenant_id=tenant_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
