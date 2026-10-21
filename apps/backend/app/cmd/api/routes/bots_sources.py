from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Request, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.knowledge.bootstrap import KnowledgeService
from app.cmd.api.deps.auth import require_auth
from app.config.config import settings
from app.domain.auth.context import AuthContext
from app.domain.knowledge.source import SourceDetail
from app.infrastructure.database.repository.bot import BotRepository
from app.infrastructure.database.repository.membership import MembershipRepository
from app.infrastructure.database.repository.source import SourceRepository
from app.infrastructure.database.session import get_session
from app.infrastructure.rabbitmq.bus import RabbitMQBus
from app.infrastructure.storage.s3 import S3ObjectStorage
from app.presenter.knowledge_http_handler import KnowledgeHTTPHandler

router = APIRouter(
    prefix="/bots",
    tags=["knowledge"],
    dependencies=[Depends(require_auth)],
)


async def get_knowledge_handler(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> KnowledgeHTTPHandler:
    storage = getattr(request.app.state, "object_storage", None)
    if storage is None:
        storage = S3ObjectStorage()
    bus = RabbitMQBus(request.app.state.rabbitmq, queue_name=settings.knowledge_queue)
    return KnowledgeHTTPHandler(
        knowledge_service=KnowledgeService(
            bot_repo=BotRepository(session),
            membership_repo=MembershipRepository(session),
            source_repo=SourceRepository(session),
            storage=storage,
            bus=bus,
        ),
    )


@router.post(
    "/{bot_id}/sources",
    response_model=SourceDetail,
    status_code=status.HTTP_201_CREATED,
)
async def upload_source(
    bot_id: UUID,
    ctx: Annotated[AuthContext, Depends(require_auth)],
    handler: Annotated[KnowledgeHTTPHandler, Depends(get_knowledge_handler)],
    file: Annotated[UploadFile, File(...)],
) -> SourceDetail:
    data = await file.read()
    return await handler.upload(
        user_id=ctx.user_id,
        bot_id=bot_id,
        filename=file.filename or "upload",
        content_type=file.content_type or "application/octet-stream",
        data=data,
    )
