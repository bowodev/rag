from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.user import IUserRepo
from app.infrastructure.database.enum import PlatformRole
from app.infrastructure.database.model.conversation import Conversation
from app.infrastructure.database.model.source import Source
from app.infrastructure.database.model.user import User


class UserRepository(IUserRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        q: str | None = None,
        platform_role: PlatformRole | None = None,
    ) -> list[User]:
        stmt = select(User)
        if q:
            pattern = f"%{q}%"
            stmt = stmt.where(
                or_(User.email.ilike(pattern), User.name.ilike(pattern))
            )
        if platform_role is not None:
            stmt = stmt.where(User.platform_role == platform_role)
        stmt = stmt.order_by(User.email)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        *,
        email: str,
        name: str,
        password_hash: str | None,
        platform_role: PlatformRole,
    ) -> User:
        user = User(
            id=uuid4(),
            email=email,
            name=name,
            password_hash=password_hash,
            platform_role=platform_role,
        )
        self._session.add(user)
        await self._session.flush()
        return user

    async def update(
        self,
        user: User,
        *,
        email: str | None = None,
        name: str | None = None,
        password_hash: str | None = None,
        clear_password: bool = False,
        platform_role: PlatformRole | None = None,
    ) -> User:
        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if clear_password:
            user.password_hash = None
        elif password_hash is not None:
            user.password_hash = password_hash
        if platform_role is not None:
            user.platform_role = platform_role
        await self._session.flush()
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.flush()

    async def count_blocking_refs(self, *, user_id: UUID) -> int:
        conv = await self._session.execute(
            select(func.count())
            .select_from(Conversation)
            .where(Conversation.user_id == user_id)
        )
        src = await self._session.execute(
            select(func.count()).select_from(Source).where(Source.user_id == user_id)
        )
        return int(conv.scalar_one()) + int(src.scalar_one())
