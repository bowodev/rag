from app.application.membership.ops_crud import (
    CreateMembership,
    DeleteMembership,
    GetMembership,
    ListMemberships,
    UpdateMembership,
)
from app.application.ports.membership import IMembershipRepo
from app.application.ports.tenant import ITenantRepo
from app.application.ports.user import IUserRepo


class OpsMembershipService:
    def __init__(
        self,
        membership_repo: IMembershipRepo,
        tenant_repo: ITenantRepo,
        user_repo: IUserRepo,
    ) -> None:
        self.list = ListMemberships(membership_repo)
        self.get = GetMembership(membership_repo)
        self.create = CreateMembership(membership_repo, tenant_repo, user_repo)
        self.update = UpdateMembership(membership_repo)
        self.delete = DeleteMembership(membership_repo)
