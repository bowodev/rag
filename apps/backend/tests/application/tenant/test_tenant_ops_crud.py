from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest

from app.application.tenant.ops_crud import CreateTenant, DeleteTenant, ListTenants
from app.domain.errors import ConflictError, NotFoundError
from app.infrastructure.database.enum import TenantStatus


@dataclass
class FakeTenant:
    id: UUID
    name: str
    slug: str
    status: TenantStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class FakeTenantRepo:
    def __init__(self) -> None:
        self.tenants: dict[UUID, FakeTenant] = {}
        self.by_slug: dict[str, FakeTenant] = {}
        self.bot_counts: dict[UUID, int] = {}

    async def get_by_id(self, tenant_id: UUID):
        return self.tenants.get(tenant_id)

    async def get_by_slug(self, slug: str):
        return self.by_slug.get(slug)

    async def list(self, *, q=None, status=None):  # noqa: ANN001
        rows = list(self.tenants.values())
        if q:
            rows = [t for t in rows if q.lower() in t.name.lower() or q.lower() in t.slug]
        if status is not None:
            rows = [t for t in rows if t.status == status]
        return rows

    async def create(self, *, name, slug, status):  # noqa: ANN001
        tenant = FakeTenant(id=uuid4(), name=name, slug=slug, status=status)
        self.tenants[tenant.id] = tenant
        self.by_slug[slug] = tenant
        return tenant

    async def delete(self, tenant):  # noqa: ANN001
        self.tenants.pop(tenant.id, None)
        self.by_slug.pop(tenant.slug, None)

    async def count_bots(self, *, tenant_id: UUID) -> int:
        return self.bot_counts.get(tenant_id, 0)


class FakeMembershipRepo:
    def __init__(self) -> None:
        self.deleted_for: list[UUID] = []

    async def delete_for_tenant(self, *, tenant_id: UUID) -> int:
        self.deleted_for.append(tenant_id)
        return 1


@pytest.mark.asyncio
async def test_create_and_list_tenants() -> None:
    repo = FakeTenantRepo()
    created = await CreateTenant(repo)(name="Acme", slug="acme")
    rows = await ListTenants(repo)(q="acm")
    assert created.slug == "acme"
    assert len(rows) == 1


@pytest.mark.asyncio
async def test_create_tenant_duplicate_slug() -> None:
    repo = FakeTenantRepo()
    await CreateTenant(repo)(name="Acme", slug="acme")
    with pytest.raises(ConflictError):
        await CreateTenant(repo)(name="Other", slug="acme")


@pytest.mark.asyncio
async def test_delete_tenant_cascades_memberships() -> None:
    tenants = FakeTenantRepo()
    memberships = FakeMembershipRepo()
    created = await CreateTenant(tenants)(name="Acme", slug="acme")
    await DeleteTenant(tenants, memberships)(tenant_id=created.id)
    assert created.id in memberships.deleted_for
    assert await tenants.get_by_id(created.id) is None


@pytest.mark.asyncio
async def test_delete_tenant_conflict_with_bots() -> None:
    tenants = FakeTenantRepo()
    memberships = FakeMembershipRepo()
    created = await CreateTenant(tenants)(name="Acme", slug="acme")
    tenants.bot_counts[created.id] = 2
    with pytest.raises(ConflictError):
        await DeleteTenant(tenants, memberships)(tenant_id=created.id)


@pytest.mark.asyncio
async def test_delete_tenant_not_found() -> None:
    with pytest.raises(NotFoundError):
        await DeleteTenant(FakeTenantRepo(), FakeMembershipRepo())(tenant_id=uuid4())
