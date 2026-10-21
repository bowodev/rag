from uuid import UUID

from app.application.ports.user import IUserRepo, UserRecord


class GetUserByID:
    def __init__(self, users: IUserRepo) -> None:
        self._users = users

    async def __call__(self, *, user_id: UUID) -> UserRecord | None:
        return await self._users.get_by_id(user_id)
