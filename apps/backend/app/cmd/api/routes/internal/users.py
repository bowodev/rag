from typing import Annotated
from uuid import UUID

from pydantic import BaseModel

from app.application.user.bootstrap import OpsUserService
from app.cmd.api.deps.auth import require_ops
from app.domain.auth.context import AuthContext
from app.domain.user.detail import UserDetail
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.repository.user import UserRepository
from app.infrastructure.database.session import get_session
from app.presenter.ops_user_http_handler import OpsUserHTTPHandler
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/users",
    tags=["internal-users"],
    dependencies=[Depends(require_ops)],
)


class CreateUserBody(BaseModel):
    email: str
    name: str
    password: str | None = None
    platform_role: str = "user"


class UpdateUserBody(BaseModel):
    email: str | None = None
    name: str | None = None
    password: str | None = None
    platform_role: str | None = None


async def get_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OpsUserHTTPHandler:
    return OpsUserHTTPHandler(
        OpsUserService(
            user_repo=UserRepository(session),
            membership_repo=MembershipRepository(session),
        )
    )


@router.get("", response_model=list[UserDetail])
async def list_users(
    handler: Annotated[OpsUserHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
    q: Annotated[str | None, Query()] = None,
    platform_role: Annotated[str | None, Query()] = None,
):
    return await handler.list(q=q, platform_role=platform_role)


@router.post("", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserBody,
    handler: Annotated[OpsUserHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.create(
        email=body.email,
        name=body.name,
        password=body.password,
        platform_role=body.platform_role,
    )


@router.get("/{user_id}", response_model=UserDetail)
async def get_user(
    user_id: UUID,
    handler: Annotated[OpsUserHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.get(user_id=user_id)


@router.patch("/{user_id}", response_model=UserDetail)
async def update_user(
    user_id: UUID,
    body: UpdateUserBody,
    handler: Annotated[OpsUserHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    return await handler.update(
        user_id=user_id,
        email=body.email,
        name=body.name,
        password=body.password,
        platform_role=body.platform_role,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    handler: Annotated[OpsUserHTTPHandler, Depends(get_handler)],
    _: Annotated[AuthContext, Depends(require_ops)],
):
    await handler.delete(user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
