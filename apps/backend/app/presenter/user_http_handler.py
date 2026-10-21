from uuid import UUID

from fastapi import status
from pydantic import BaseModel

from app.application.ports.user import IUserService
from app.cmd.api.errors import api_error


class UserResponse(BaseModel):
    id: UUID
    email: str


class UserHTTPHandler:
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    async def get_user(self, user_id: UUID) -> UserResponse:
        user = await self._user_service.get_by_id(user_id=user_id)
        if user is None:
            raise api_error(
                status.HTTP_404_NOT_FOUND,
                message="failed to get user",
                error="user not found",
            )
        return UserResponse(id=user.id, email=user.email)
