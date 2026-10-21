from uuid import UUID

from fastapi import status

from app.application.bot.bootstrap import BotService
from app.cmd.api.errors import api_error
from app.domain.bot.summary import BotSummary
from app.domain.errors import ForbiddenError


class BotHTTPHandler:
    def __init__(self, bot_service: BotService) -> None:
        self._bots = bot_service

    async def list_for_user(self, *, user_id: UUID) -> list[BotSummary]:
        try:
            return await self._bots.list_for_user(user_id=user_id)
        except Exception as e:
            raise api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="failed to list bots",
                error="an unexpected error occurred",
            ) from e

    async def get_for_user(self, *, user_id: UUID, bot_id: UUID) -> BotSummary:
        try:
            return await self._bots.get_for_user(user_id=user_id, bot_id=bot_id)
        except ForbiddenError as e:
            raise api_error(
                status.HTTP_403_FORBIDDEN,
                message="failed to get bot",
                error=str(e) or "bot access denied",
            ) from e
        except Exception as e:
            raise api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="failed to get bot",
                error="an unexpected error occurred",
            ) from e
