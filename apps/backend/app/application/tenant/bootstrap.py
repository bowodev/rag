from app.application.ports.membership import IMembershipRepo
from app.application.ports.tenant import ITenantRepo
from app.application.tenant.list_for_user import ListTenantsForUser
from app.application.tenant.ops_crud import (
    CreateTenant,
    DeleteTenant,
    GetTenant,
    ListTenants,
    UpdateTenant,
)


class TenantService:
    def __init__(self, membership_repo: IMembershipRepo) -> None:
        self.list_for_user = ListTenantsForUser(membership_repo)


class OpsTenantService:
    def __init__(self, tenant_repo: ITenantRepo, membership_repo: IMembershipRepo) -> None:
        self.list = ListTenants(tenant_repo)
        self.get = GetTenant(tenant_repo)
        self.create = CreateTenant(tenant_repo)
        self.update = UpdateTenant(tenant_repo)
        self.delete = DeleteTenant(tenant_repo, membership_repo)
