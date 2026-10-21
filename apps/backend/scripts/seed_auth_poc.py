"""Seed one active tenant + membership + user for auth smoke tests.

Usage (from apps/backend):
  uv run python scripts/seed_auth_poc.py
"""

from __future__ import annotations

import asyncio
import uuid

from sqlalchemy import select

from app.application.auth.password_helper import hash_password
from app.infrastructure.database.enum import MembershipRole, TenantStatus
from app.infrastructure.database.model.membership import Membership
from app.infrastructure.database.model.tenant import Tenant
from app.infrastructure.database.model.user import User
from app.infrastructure.database.session import SessionLocal

SEED_EMAIL = "demo@virtuascope.local"
SEED_PASSWORD = "demo-password"
SEED_TENANT_SLUG = "demo"


async def seed() -> None:
    async with SessionLocal() as session:
        existing = await session.execute(select(User).where(User.email == SEED_EMAIL))
        user = existing.scalar_one_or_none()
        if user is None:
            user = User(
                id=uuid.uuid4(),
                email=SEED_EMAIL,
                name="Demo User",
                password_hash=hash_password(SEED_PASSWORD),
            )
            session.add(user)
        elif not user.password_hash:
            user.password_hash = hash_password(SEED_PASSWORD)

        tenant_result = await session.execute(
            select(Tenant).where(Tenant.slug == SEED_TENANT_SLUG)
        )
        tenant = tenant_result.scalar_one_or_none()
        if tenant is None:
            tenant = Tenant(
                id=uuid.uuid4(),
                name="Demo Tenant",
                slug=SEED_TENANT_SLUG,
                status=TenantStatus.ACTIVE,
            )
            session.add(tenant)

        await session.flush()

        membership_result = await session.execute(
            select(Membership).where(
                Membership.user_id == user.id,
                Membership.tenant_id == tenant.id,
            )
        )
        if membership_result.scalar_one_or_none() is None:
            session.add(
                Membership(
                    id=uuid.uuid4(),
                    tenant_id=tenant.id,
                    user_id=user.id,
                    role=MembershipRole.OWNER,
                )
            )

        await session.commit()
        print(f"seeded user={SEED_EMAIL} password={SEED_PASSWORD} tenant={SEED_TENANT_SLUG}")


if __name__ == "__main__":
    asyncio.run(seed())
