from dataclasses import dataclass
from uuid import uuid4

import pytest

from app.application.tenant.list_for_user import ListTenantsForUser


@dataclass
class FakeRow:
    id: object
    name: str
    slug: str
    status: str
    role: str


class FakeMembershipRepo:
    def __init__(self, rows: list[FakeRow]) -> None:
        self._rows = rows
        self.calls: list[object] = []

    async def list_tenants_for_user(self, *, user_id):  # noqa: ANN001
        self.calls.append(user_id)
        return self._rows

    async def has_membership(self, *, user_id, tenant_id) -> bool:  # noqa: ANN001
        return False


@pytest.mark.asyncio
async def test_list_tenants_for_user_maps_rows() -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    rows = [
        FakeRow(
            id=tenant_id,
            name="Acme",
            slug="acme",
            status="active",
            role="owner",
        )
    ]
    result = await ListTenantsForUser(FakeMembershipRepo(rows))(user_id=user_id)
    assert len(result) == 1
    assert result[0].id == tenant_id
    assert result[0].slug == "acme"
    assert result[0].role == "owner"
