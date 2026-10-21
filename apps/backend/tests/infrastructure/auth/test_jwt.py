from uuid import uuid4

import pytest

from app.infrastructure.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)


def test_access_and_refresh_type_guards() -> None:
    user_id = uuid4()
    access = create_access_token(user_id=user_id)
    refresh = create_refresh_token(user_id=user_id)

    assert decode_access_token(access)["sub"] == str(user_id)
    assert decode_refresh_token(refresh)["sub"] == str(user_id)

    with pytest.raises(ValueError, match="invalid token type"):
        decode_access_token(refresh)
    with pytest.raises(ValueError, match="invalid token type"):
        decode_refresh_token(access)
