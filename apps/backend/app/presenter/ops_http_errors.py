from collections.abc import Awaitable, Callable
from typing import TypeVar

from fastapi import status

from app.cmd.api.errors import api_error
from app.domain.errors import ConflictError, NotFoundError, ValidationError

T = TypeVar("T")


async def map_ops_errors(
    *,
    message: str,
    call: Callable[[], Awaitable[T]],
) -> T:
    try:
        return await call()
    except ValidationError as e:
        raise api_error(
            status.HTTP_400_BAD_REQUEST,
            message=message,
            error=str(e) or "validation failed",
        ) from e
    except NotFoundError as e:
        raise api_error(
            status.HTTP_404_NOT_FOUND,
            message=message,
            error=str(e) or "not found",
        ) from e
    except ConflictError as e:
        raise api_error(
            status.HTTP_409_CONFLICT,
            message=message,
            error=str(e) or "conflict",
        ) from e
    except Exception as e:
        raise api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error="an unexpected error occurred",
        ) from e
