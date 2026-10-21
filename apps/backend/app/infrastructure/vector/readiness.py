from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession


async def assert_vector_store_ready(conn: AsyncConnection | AsyncSession) -> None:
    """Fail if pgvector extension or chunk_embeddings table is missing."""
    ext = await conn.execute(
        text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
    )
    if ext.scalar() is None:
        raise RuntimeError("pgvector extension not installed")

    table = await conn.execute(
        text(
            "SELECT 1 FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_name = 'chunk_embeddings'"
        )
    )
    if table.scalar() is None:
        raise RuntimeError("chunk_embeddings table missing")
