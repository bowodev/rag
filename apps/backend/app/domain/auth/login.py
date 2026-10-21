from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str


@dataclass(frozen=True)
class RefreshRequest:
    refresh_token: str


@dataclass(frozen=True)
class SetPasswordRequest:
    email: str
    password: str


@dataclass(frozen=True)
class LoginResponse:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user_id: UUID
    email: str
