# app/infrastructure/auth/jwt.py
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import jwt
from app.config.config import settings
from jwt import InvalidTokenError

_TOKEN_TYPE_ACCESS = "access"
_TOKEN_TYPE_REFRESH = "refresh"


def create_access_token(*, user_id: UUID) -> str:
    return _encode_token(
        user_id=user_id,
        token_type=_TOKEN_TYPE_ACCESS,
        ttl_seconds=settings.jwt_ttl_seconds,
    )


def create_refresh_token(*, user_id: UUID) -> str:
    return _encode_token(
        user_id=user_id,
        token_type=_TOKEN_TYPE_REFRESH,
        ttl_seconds=settings.jwt_refresh_ttl_seconds,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return _decode_token(token, expected_type=_TOKEN_TYPE_ACCESS)


def decode_refresh_token(token: str) -> dict[str, Any]:
    return _decode_token(token, expected_type=_TOKEN_TYPE_REFRESH)


def _encode_token(*, user_id: UUID, token_type: str, ttl_seconds: int) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(seconds=ttl_seconds),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def _decode_token(token: str, *, expected_type: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except InvalidTokenError as exc:
        raise ValueError("invalid token") from exc

    if payload.get("type") != expected_type:
        raise ValueError("invalid token type")
    return payload
