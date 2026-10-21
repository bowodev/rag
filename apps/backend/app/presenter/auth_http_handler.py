from fastapi import status

from app.application.ports.auth import IAuthService
from app.cmd.api.errors import api_error
from app.domain.auth.login import LoginResponse
from app.domain.errors import ConflictError, UnauthorizedError, ValidationError


class AuthHTTPHandler:
    def __init__(self, auth_service: IAuthService) -> None:
        self._auth_service = auth_service

    async def login(self, *, email: str, password: str) -> LoginResponse:
        try:
            return await self._auth_service.login(email=email, password=password)
        except ValidationError as e:
            raise api_error(
                status.HTTP_400_BAD_REQUEST,
                message="failed to login",
                error=str(e) or "validation failed",
            ) from e
        except UnauthorizedError as e:
            raise api_error(
                status.HTTP_401_UNAUTHORIZED,
                message="failed to login",
                error=str(e) or "invalid credentials",
            ) from e
        except Exception as e:
            raise api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="failed to login",
                error="an unexpected error occurred",
            ) from e

    async def refresh(self, *, refresh_token: str) -> LoginResponse:
        try:
            return await self._auth_service.refresh(refresh_token=refresh_token)
        except ValidationError as e:
            raise api_error(
                status.HTTP_400_BAD_REQUEST,
                message="failed to refresh token",
                error=str(e) or "validation failed",
            ) from e
        except UnauthorizedError as e:
            raise api_error(
                status.HTTP_401_UNAUTHORIZED,
                message="failed to refresh token",
                error=str(e) or "invalid token",
            ) from e
        except Exception as e:
            raise api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="failed to refresh token",
                error="an unexpected error occurred",
            ) from e

    async def set_password(self, *, email: str, password: str) -> None:
        try:
            await self._auth_service.set_password(email=email, password=password)
        except ValidationError as e:
            raise api_error(
                status.HTTP_400_BAD_REQUEST,
                message="failed to set password",
                error=str(e) or "validation failed",
            ) from e
        except ConflictError as e:
            raise api_error(
                status.HTTP_409_CONFLICT,
                message="failed to set password",
                error=str(e) or "password cannot be set",
            ) from e
        except Exception as e:
            raise api_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="failed to set password",
                error="an unexpected error occurred",
            ) from e
