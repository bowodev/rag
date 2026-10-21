from uuid import UUID, uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.tenant import ITenantRepo
from app.infrastructure.database.enum import TenantStatus
from app.infrastructure.database.model.bot import Bot
from app.infrastructure.database.model.tenant import Tenant


class TenantRepository(ITenantRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, tenant_id: UUID) -> Tenant | None:
        return await self._session.get(Tenant, tenant_id)

    async def get_by_slug(self, slug: str) -> Tenant | None:
        result = await self._session.execute(select(Tenant).where(Tenant.slug == slug))
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        q: str | None = None,
        status: TenantStatus | None = None,
    ) -> list[Tenant]:
        stmt = select(Tenant)
        if q:
            pattern = f"%{q}%"
            stmt = stmt.where(
                or_(Tenant.name.ilike(pattern), Tenant.slug.ilike(pattern))
            )
        if status is not None:
            stmt = stmt.where(Tenant.status == status)
        stmt = stmt.order_by(Tenant.name)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        *,
        name: str,
        slug: str,
        status: TenantStatus,
    ) -> Tenant:
        tenant = Tenant(id=uuid4(), name=name, slug=slug, status=status)
        self._session.add(tenant)
        await self._session.flush()
        return tenant

    async def update(
        self,
        tenant: Tenant,
        *,
        name: str | None = None,
        slug: str | None = None,
        status: TenantStatus | None = None,
    ) -> Tenant:
        if name is not None:
            tenant.name = name
        if slug is not None:
            tenant.slug = slug
        if status is not None:
            tenant.status = status
        await self._session.flush()
        return tenant

    async def delete(self, tenant: Tenant) -> None:
        await self._session.delete(tenant)
        await self._session.flush()

    async def count_bots(self, *, tenant_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(Bot).where(Bot.tenant_id == tenant_id)
        )
        return int(result.scalar_one())
