from typing import Protocol

from app.domain.auth.login import LoginResponse


class IAuthService(Protocol):
    async def login(self, *, email: str, password: str) -> LoginResponse: ...

    async def refresh(self, *, refresh_token: str) -> LoginResponse: ...

    async def set_password(self, *, email: str, password: str) -> None: ...
