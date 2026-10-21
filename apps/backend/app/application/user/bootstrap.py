from app.application.ports.membership import IMembershipRepo
from app.application.ports.user import IUserRepo, IUserService
from app.application.user.get_by_id import GetUserByID
from app.application.user.ops_crud import (
    CreateUser,
    DeleteUser,
    GetUser,
    ListUsers,
    UpdateUser,
)


class UserService(IUserService):
    def __init__(self, user_repo: IUserRepo) -> None:
        self.get_by_id = GetUserByID(user_repo)


class OpsUserService:
    def __init__(self, user_repo: IUserRepo, membership_repo: IMembershipRepo) -> None:
        self.list = ListUsers(user_repo)
        self.get = GetUser(user_repo)
        self.create = CreateUser(user_repo)
        self.update = UpdateUser(user_repo)
        self.delete = DeleteUser(user_repo, membership_repo)
