from uuid import UUID

from app.application.bot.map_summary import to_bot_summary
from app.application.ports.bot import IBotRepo
from app.application.ports.membership import IMembershipRepo
from app.domain.bot.summary import BotSummary
from app.domain.errors import ForbiddenError


class GetBotForUser:
    def __init__(self, bots: IBotRepo, memberships: IMembershipRepo) -> None:
        self._bots = bots
        self._memberships = memberships

    async def __call__(self, *, user_id: UUID, bot_id: UUID) -> BotSummary:
        bot = await self._bots.get_by_id(bot_id=bot_id)
        if bot is None:
            raise ForbiddenError("bot access denied")
        allowed = await self._memberships.has_membership(
            user_id=user_id,
            tenant_id=bot.tenant_id,
        )
        if not allowed:
            raise ForbiddenError("bot access denied")
        return to_bot_summary(bot)
