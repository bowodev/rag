"""VCS-001 subtask 10 — models import, migrations applied, vector store reachable."""

import pytest
from sqlalchemy import text

from app.infrastructure.database.model import (
    Bot,
    Chunk,
    ChunkEmbedding,
    Conversation,
    Membership,
    Message,
    Source,
    Tenant,
    User,
)
from app.infrastructure.database.session import SessionLocal, engine
from app.infrastructure.vector.readiness import assert_vector_store_ready

EXPECTED_TABLES = {
    "tenants",
    "users",
    "memberships",
    "bots",
    "sources",
    "chunks",
    "chunk_embeddings",
    "conversations",
    "messages",
}


def test_domain_models_import() -> None:
    assert Tenant.__tablename__ == "tenants"
    assert User.__tablename__ == "users"
    assert Membership.__tablename__ == "memberships"
    assert Bot.__tablename__ == "bots"
    assert Source.__tablename__ == "sources"
    assert Chunk.__tablename__ == "chunks"
    assert ChunkEmbedding.__tablename__ == "chunk_embeddings"
    assert Conversation.__tablename__ == "conversations"
    assert Message.__tablename__ == "messages"
    assert not hasattr(Bot, "system_prompt")
    assert not hasattr(Bot, "model")
    assert not hasattr(Bot, "temperature")


@pytest.mark.asyncio
async def test_migrations_and_vector_store() -> None:
    async with engine.connect() as conn:
        rows = await conn.execute(
            text(
                "SELECT tablename FROM pg_tables "
                "WHERE schemaname = 'public' AND tablename = ANY(:names)"
            ),
            {"names": list(EXPECTED_TABLES)},
        )
        found = {r[0] for r in rows}
        missing = EXPECTED_TABLES - found
        assert not missing, f"missing tables: {sorted(missing)}"

        await assert_vector_store_ready(conn)

    async with SessionLocal() as session:
        await assert_vector_store_ready(session)
