from typing import Annotated
from uuid import UUID

from app.application.bot.bootstrap import BotService
from app.cmd.api.deps.auth import require_auth
from app.domain.auth.context import AuthContext
from app.domain.bot.summary import BotSummary
from app.infrastructure.database.repository.bot import BotRepository
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.session import get_session
from app.presenter.bot_http_handler import BotHTTPHandler
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/bots",
    tags=["bots"],
    dependencies=[Depends(require_auth)],
)


async def get_bot_handler(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> BotHTTPHandler:
    return BotHTTPHandler(
        bot_service=BotService(
            bot_repo=BotRepository(session),
            membership_repo=MembershipRepository(session),
        ),
    )


@router.get("", response_model=list[BotSummary])
async def list_bots(
    ctx: Annotated[AuthContext, Depends(require_auth)],
    handler: Annotated[BotHTTPHandler, Depends(get_bot_handler)],
) -> list[BotSummary]:
    return await handler.list_for_user(user_id=ctx.user_id)


@router.get("/{bot_id}", response_model=BotSummary)
async def get_bot(
    bot_id: UUID,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    handler: Annotated[BotHTTPHandler, Depends(get_bot_handler)],
) -> BotSummary:
    return await handler.get_for_user(user_id=ctx.user_id, bot_id=bot_id)
