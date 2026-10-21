from uuid import UUID

from app.application.bot.map_summary import to_bot_summary
from app.application.ports.bot import IBotRepo
from app.application.ports.membership import IMembershipRepo
from app.domain.bot.summary import BotSummary


class ListBotsForUser:
    def __init__(self, bots: IBotRepo, memberships: IMembershipRepo) -> None:
        self._bots = bots
        self._memberships = memberships

    async def __call__(self, *, user_id: UUID) -> list[BotSummary]:
        tenants = await self._memberships.list_tenants_for_user(user_id=user_id)
        if not tenants:
            return []
        bots = await self._bots.list_by_tenant_ids(
            tenant_ids=[tenant.id for tenant in tenants]
        )
        return [to_bot_summary(bot) for bot in bots]
