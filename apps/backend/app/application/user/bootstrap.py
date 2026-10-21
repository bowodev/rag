from app.application.ports.user import IUserRepo, IUserService
from app.application.user.get_by_id import GetUserByID


class UserService(IUserService):
    def __init__(self, user_repo: IUserRepo) -> None:
        self.get_by_id = GetUserByID(user_repo)
