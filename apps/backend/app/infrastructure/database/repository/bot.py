from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.bot import IBotRepo
from app.infrastructure.database.model.bot import Bot


class BotRepository(IBotRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, *, bot_id: UUID) -> Bot | None:
        return await self._session.get(Bot, bot_id)

    async def list_by_tenant_ids(self, *, tenant_ids: Sequence[UUID]) -> list[Bot]:
        if not tenant_ids:
            return []
        stmt = (
            select(Bot)
            .where(Bot.tenant_id.in_(list(tenant_ids)))
            .order_by(Bot.name, Bot.id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
