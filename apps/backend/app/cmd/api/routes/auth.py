from typing import Annotated

from app.application.auth.bootstrap import AuthService
from app.domain.auth.login import LoginRequest, LoginResponse, RefreshRequest
from app.infrastructure.database.repository.user import UserRepository
from app.infrastructure.database.session import get_session
from app.presenter.auth_http_handler import AuthHTTPHandler
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


async def get_auth_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthHTTPHandler:
    return AuthHTTPHandler(
        auth_service=AuthService(user_repo=UserRepository(session)),
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    handler: Annotated[AuthHTTPHandler, Depends(get_auth_handler)],
):
    return await handler.login(email=request.email, password=request.password)


@router.post("/refresh", response_model=LoginResponse)
async def refresh(
    request: RefreshRequest,
    handler: Annotated[AuthHTTPHandler, Depends(get_auth_handler)],
):
    return await handler.refresh(refresh_token=request.refresh_token)
