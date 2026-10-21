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

Env (see `.env.example`): `DATABASE_URL`, `EMBEDDING_DIMENSION` (default 1536),
S3/MinIO (`S3_*`), JWT, RabbitMQ knowledge queues.

## Knowledge upload (VCS-005)

- `POST /bots/{bot_id}/sources` — multipart file (PDF/TXT/DOCX, ≤10 MB)
- Raw files → MinIO; Source row `processing`; job → `knowledge.index`
- Consumers: `knowledge-recovery` (republish stuck), `knowledge-dlq` (mark `failed`)

```bash
make infra-up                 # includes MinIO :9000 / console :9001
make backend-consumer-dlq
make backend-consumer-recovery
```
