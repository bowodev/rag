from uuid import UUID

from app.application.tenant.bootstrap import OpsTenantService
from app.domain.tenant.detail import TenantDetail
from app.presenter.ops_http_errors import map_ops_errors


class OpsTenantHTTPHandler:
    def __init__(self, service: OpsTenantService) -> None:
        self._service = service

    async def list(
        self, *, q: str | None = None, status: str | None = None
    ) -> list[TenantDetail]:
        return await map_ops_errors(
            message="failed to list tenants",
            call=lambda: self._service.list(q=q, status=status),
        )

    async def get(self, *, tenant_id: UUID) -> TenantDetail:
        return await map_ops_errors(
            message="failed to get tenant",
            call=lambda: self._service.get(tenant_id=tenant_id),
        )

    async def create(
        self, *, name: str, slug: str, status: str = "active"
    ) -> TenantDetail:
        return await map_ops_errors(
            message="failed to create tenant",
            call=lambda: self._service.create(name=name, slug=slug, status=status),
        )

    async def update(
        self,
        *,
        tenant_id: UUID,
        name: str | None = None,
        slug: str | None = None,
        status: str | None = None,
    ) -> TenantDetail:
        return await map_ops_errors(
            message="failed to update tenant",
            call=lambda: self._service.update(
                tenant_id=tenant_id, name=name, slug=slug, status=status
            ),
        )

    async def delete(self, *, tenant_id: UUID) -> None:
        await map_ops_errors(
            message="failed to delete tenant",
            call=lambda: self._service.delete(tenant_id=tenant_id),
        )
