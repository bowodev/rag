from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.bot import IBotRepo
from app.infrastructure.database.model.bot import Bot


class BotRepository(IBotRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, *, bot_id: UUID) -> Bot | None:
        return await self._session.get(Bot, bot_id)
