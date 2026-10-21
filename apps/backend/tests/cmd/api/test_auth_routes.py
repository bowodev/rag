"""HTTP-level auth route smoke tests with mocked lifespan + services."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

from starlette.testclient import TestClient

from app.cmd.api.main import app
from app.domain.auth.context import AuthContext
from app.domain.auth.login import LoginResponse
from app.domain.tenant.summary import TenantSummary
from app.infrastructure.auth.jwt import create_access_token, create_refresh_token


def _client():
    mock_conn = AsyncMock()
    mock_conn.close = AsyncMock()
    return patch(
        "app.cmd.api.main.get_connection",
        new=AsyncMock(return_value=mock_conn),
    )


def test_me_requires_auth() -> None:
    with _client():
        with TestClient(app) as client:
            res = client.get("/me")
            assert res.status_code == 401


def test_me_with_valid_access_token() -> None:
    user_id = uuid4()
    token = create_access_token(user_id=user_id)
    ctx = AuthContext(user_id=user_id, email="a@example.com")

    async def fake_require_auth():  # noqa: ANN202
        return ctx

    with _client():
        app.dependency_overrides.clear()
        from app.cmd.api.deps import auth as auth_deps

        app.dependency_overrides[auth_deps.require_auth] = fake_require_auth
        try:
            with TestClient(app) as client:
                # Override short-circuits DB; still send Bearer for realism.
                res = client.get(
                    "/me",
                    headers={"Authorization": f"Bearer {token}"},
                )
                assert res.status_code == 200
                assert res.json()["email"] == "a@example.com"
                assert res.json()["user_id"] == str(user_id)
        finally:
            app.dependency_overrides.clear()


def test_tenants_requires_auth() -> None:
    with _client():
        with TestClient(app) as client:
            res = client.get("/tenants")
            assert res.status_code == 401


def test_tenants_returns_membership_list() -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    ctx = AuthContext(user_id=user_id, email="a@example.com")

    async def fake_require_auth():  # noqa: ANN202
        return ctx

    class FakeHandler:
        async def list_for_user(self, *, user_id):  # noqa: ANN001
            assert user_id == ctx.user_id
            return [
                TenantSummary(
                    id=tenant_id,
                    name="Demo",
                    slug="demo",
                    status="active",
                    role="owner",
                )
            ]

    async def fake_handler():  # noqa: ANN202
        return FakeHandler()

    with _client():
        from app.cmd.api.deps import auth as auth_deps
        from app.cmd.api.routes import tenants as tenants_route

        app.dependency_overrides[auth_deps.require_auth] = fake_require_auth
        app.dependency_overrides[tenants_route.get_tenant_handler] = fake_handler
        try:
            with TestClient(app) as client:
                res = client.get(
                    "/tenants",
                    headers={"Authorization": f"Bearer {create_access_token(user_id=user_id)}"},
                )
                assert res.status_code == 200
                body = res.json()
                assert len(body) == 1
                assert body[0]["slug"] == "demo"
        finally:
            app.dependency_overrides.clear()


def test_users_by_id_route_removed() -> None:
    with _client():
        with TestClient(app) as client:
            res = client.get(f"/users/{uuid4()}")
            assert res.status_code == 404


def test_refresh_endpoint_wired() -> None:
    user_id = uuid4()
    refresh = create_refresh_token(user_id=user_id)
    expected = LoginResponse(
        access_token="a",
        refresh_token="r",
        token_type="Bearer",
        expires_in=3600,
        user_id=user_id,
        email="a@example.com",
    )

    class FakeHandler:
        async def refresh(self, *, refresh_token: str):
            assert refresh_token == refresh
            return expected

        async def login(self, *, email: str, password: str):  # pragma: no cover
            raise AssertionError("login should not be called")

    async def fake_handler():  # noqa: ANN202
        return FakeHandler()

    with _client():
        from app.cmd.api.routes import auth as auth_route

        app.dependency_overrides[auth_route.get_auth_handler] = fake_handler
        try:
            with TestClient(app) as client:
                res = client.post("/auth/refresh", json={"refresh_token": refresh})
                assert res.status_code == 200
                assert res.json()["access_token"] == "a"
        finally:
            app.dependency_overrides.clear()
