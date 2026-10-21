from typing import Annotated
from uuid import UUID

from pydantic import BaseModel

from app.application.membership.bootstrap import OpsMembershipService
from app.cmd.api.deps.auth import require_ops
from app.domain.auth.context import AuthContext
from app.domain.membership.detail import MembershipDetail
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.repository.tenant import TenantRepository
from app.infrastructure.database.repository.user import UserRepository
from app.infrastructure.database.session import get_session
from app.presenter.ops_membership_http_handler import OpsMembershipHTTPHandler
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/memberships",
    tags=["internal-memberships"],
    dependencies=[Depends(require_ops)],
)


class CreateMembershipBody(BaseModel):
    tenant_id: UUID
    user_id: UUID
    role: str = "member"


class UpdateMembershipBody(BaseModel):
    role: str


async def get_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OpsMembershipHTTPHandler:
    return OpsMembershipHTTPHandler(
        OpsMembershipService(
            membership_repo=MembershipRepository(session),
            tenant_repo=TenantRepository(session),
            user_repo=UserRepository(session),
        )
    )


@router.get("", response_model=list[MembershipDetail])
async def list_memberships(
    handler: Annotated[OpsMembershipHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
    tenant_id: Annotated[UUID | None, Query()] = None,
    user_id: Annotated[UUID | None, Query()] = None,
):
    return await handler.list(tenant_id=tenant_id, user_id=user_id)


@router.post("", response_model=MembershipDetail, status_code=status.HTTP_201_CREATED)
async def create_membership(
    body: CreateMembershipBody,
    handler: Annotated[OpsMembershipHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.create(
        tenant_id=body.tenant_id,
        user_id=body.user_id,
        role=body.role,
    )


@router.get("/{membership_id}", response_model=MembershipDetail)
async def get_membership(
    membership_id: UUID,
    handler: Annotated[OpsMembershipHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.get(membership_id=membership_id)


@router.patch("/{membership_id}", response_model=MembershipDetail)
async def update_membership(
    membership_id: UUID,
    body: UpdateMembershipBody,
    handler: Annotated[OpsMembershipHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.update(membership_id=membership_id, role=body.role)


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_membership(
    membership_id: UUID,
    handler: Annotated[OpsMembershipHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    await handler.delete(membership_id=membership_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
