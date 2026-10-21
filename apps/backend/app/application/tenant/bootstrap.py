from app.application.ports.membership import IMembershipRepo
from app.application.tenant.list_for_user import ListTenantsForUser


class TenantService:
    def __init__(self, membership_repo: IMembershipRepo) -> None:
        self.list_for_user = ListTenantsForUser(membership_repo)
