"""HTTP smoke for /internal/* and set-password."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

from starlette.testclient import TestClient

from app.cmd.api.main import app
from app.domain.auth.context import AuthContext
from app.domain.tenant.detail import TenantDetail
from datetime import datetime, timezone


def _client():
    mock_conn = AsyncMock()
    mock_conn.close = AsyncMock()
    return patch(
        "app.cmd.api.main.get_connection",
        new=AsyncMock(return_value=mock_conn),
    )


def test_internal_tenants_requires_auth() -> None:
    with _client():
        with TestClient(app) as client:
            res = client.get("/internal/tenants")
            assert res.status_code == 401


def test_internal_tenants_denies_non_ops() -> None:
    ctx = AuthContext(user_id=uuid4(), email="a@example.com", platform_role="user")

    async def fake_auth():  # noqa: ANN202
        return ctx

    with _client():
        from app.cmd.api.deps import auth as auth_deps

        app.dependency_overrides[auth_deps.require_auth] = fake_auth
        try:
            with TestClient(app) as client:
                res = client.get("/internal/tenants")
                assert res.status_code == 403
        finally:
            app.dependency_overrides.clear()


def test_internal_tenants_ops_list() -> None:
    ctx = AuthContext(user_id=uuid4(), email="ops@example.com", platform_role="ops")
    tenant_id = uuid4()
    now = datetime.now(timezone.utc)

    async def fake_auth():  # noqa: ANN202
        return ctx

    class FakeHandler:
        async def list(self, *, q=None, status=None):  # noqa: ANN001
            return [
                TenantDetail(
                    id=tenant_id,
                    name="Acme",
                    slug="acme",
                    status="active",
                    created_at=now,
                    updated_at=now,
                )
            ]

    async def fake_handler():  # noqa: ANN202
        return FakeHandler()

    with _client():
        from app.cmd.api.deps import auth as auth_deps
        from app.cmd.api.routes.internal import tenants as tenants_route

        app.dependency_overrides[auth_deps.require_auth] = fake_auth
        app.dependency_overrides[tenants_route.get_handler] = fake_handler
        try:
            with TestClient(app) as client:
                res = client.get("/internal/tenants")
                assert res.status_code == 200
                assert res.json()[0]["slug"] == "acme"
        finally:
            app.dependency_overrides.clear()


def test_set_password_endpoint_wired() -> None:
    class FakeHandler:
        async def set_password(self, *, email: str, password: str):
            assert email == "a@example.com"
            assert password == "secret12"

        async def login(self, **kwargs):  # pragma: no cover
            raise AssertionError("unused")

        async def refresh(self, **kwargs):  # pragma: no cover
            raise AssertionError("unused")

    async def fake_handler():  # noqa: ANN202
        return FakeHandler()

    with _client():
        from app.cmd.api.routes import auth as auth_route

        app.dependency_overrides[auth_route.get_auth_handler] = fake_handler
        try:
            with TestClient(app) as client:
                res = client.post(
                    "/auth/set-password",
                    json={"email": "a@example.com", "password": "secret12"},
                )
                assert res.status_code == 204
        finally:
            app.dependency_overrides.clear()
