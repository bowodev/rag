from uuid import UUID

from app.application.tenant.bootstrap import TenantService
from app.domain.tenant.summary import TenantSummary


class TenantHTTPHandler:
    def __init__(self, tenant_service: TenantService) -> None:
        self._tenant_service = tenant_service

    async def list_for_user(self, *, user_id: UUID) -> list[TenantSummary]:
        return await self._tenant_service.list_for_user(user_id=user_id)
