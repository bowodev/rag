# VCS backend

FastAPI + SQLAlchemy (async) + Alembic + RabbitMQ consumer.

## Database

Postgres with pgvector (`docker compose` service `postgres`).

```bash
# from apps/backend
uv sync
uv run alembic upgrade head
uv run pytest tests/test_vcs001_smoke.py
```

Env (see `.env.example`): `DATABASE_URL`, `EMBEDDING_DIMENSION` (default 1536).
