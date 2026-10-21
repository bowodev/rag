from app.application.auth.login import Login
from app.application.auth.refresh import Refresh
from app.application.ports.auth import IAuthService
from app.application.ports.user import IUserRepo


class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepo) -> None:
        self.login = Login(user_repo)
        self.refresh = Refresh(user_repo)
