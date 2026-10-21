from uuid import UUID

from app.application.ports.membership import IMembershipRepo
from app.application.ports.tenant import ITenantRepo
from app.domain.errors import ConflictError, NotFoundError, ValidationError
from app.domain.tenant.detail import TenantDetail
from app.infrastructure.database.enum import TenantStatus


def _to_detail(tenant) -> TenantDetail:  # noqa: ANN001
    status = tenant.status.value if hasattr(tenant.status, "value") else str(tenant.status)
    return TenantDetail(
        id=tenant.id,
        name=tenant.name,
        slug=tenant.slug,
        status=status,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


class ListTenants:
    def __init__(self, tenants: ITenantRepo) -> None:
        self._tenants = tenants

    async def __call__(
        self,
        *,
        q: str | None = None,
        status: str | None = None,
    ) -> list[TenantDetail]:
        status_enum = None
        if status:
            try:
                status_enum = TenantStatus(status)
            except ValueError as exc:
                raise ValidationError("invalid status") from exc
        rows = await self._tenants.list(q=q, status=status_enum)
        return [_to_detail(t) for t in rows]


class GetTenant:
    def __init__(self, tenants: ITenantRepo) -> None:
        self._tenants = tenants

    async def __call__(self, *, tenant_id: UUID) -> TenantDetail:
        tenant = await self._tenants.get_by_id(tenant_id)
        if tenant is None:
            raise NotFoundError("tenant not found")
        return _to_detail(tenant)


class CreateTenant:
    def __init__(self, tenants: ITenantRepo) -> None:
        self._tenants = tenants

    async def __call__(
        self,
        *,
        name: str,
        slug: str,
        status: str = TenantStatus.ACTIVE.value,
    ) -> TenantDetail:
        if not name.strip():
            raise ValidationError("name is required")
        if not slug.strip():
            raise ValidationError("slug is required")
        existing = await self._tenants.get_by_slug(slug.strip())
        if existing is not None:
            raise ConflictError("slug already exists")
        try:
            status_enum = TenantStatus(status)
        except ValueError as exc:
            raise ValidationError("invalid status") from exc
        tenant = await self._tenants.create(
            name=name.strip(),
            slug=slug.strip(),
            status=status_enum,
        )
        return _to_detail(tenant)


class UpdateTenant:
    def __init__(self, tenants: ITenantRepo) -> None:
        self._tenants = tenants

    async def __call__(
        self,
        *,
        tenant_id: UUID,
        name: str | None = None,
        slug: str | None = None,
        status: str | None = None,
    ) -> TenantDetail:
        tenant = await self._tenants.get_by_id(tenant_id)
        if tenant is None:
            raise NotFoundError("tenant not found")
        if slug is not None:
            slug = slug.strip()
            if not slug:
                raise ValidationError("slug is required")
            other = await self._tenants.get_by_slug(slug)
            if other is not None and other.id != tenant_id:
                raise ConflictError("slug already exists")
        if name is not None and not name.strip():
            raise ValidationError("name is required")
        status_enum = None
        if status is not None:
            try:
                status_enum = TenantStatus(status)
            except ValueError as exc:
                raise ValidationError("invalid status") from exc
        updated = await self._tenants.update(
            tenant,
            name=name.strip() if name is not None else None,
            slug=slug,
            status=status_enum,
        )
        return _to_detail(updated)


class DeleteTenant:
    def __init__(self, tenants: ITenantRepo, memberships: IMembershipRepo) -> None:
        self._tenants = tenants
        self._memberships = memberships

    async def __call__(self, *, tenant_id: UUID) -> None:
        tenant = await self._tenants.get_by_id(tenant_id)
        if tenant is None:
            raise NotFoundError("tenant not found")
        if await self._tenants.count_bots(tenant_id=tenant_id) > 0:
            raise ConflictError("tenant has dependent bots")
        await self._memberships.delete_for_tenant(tenant_id=tenant_id)
        await self._tenants.delete(tenant)
