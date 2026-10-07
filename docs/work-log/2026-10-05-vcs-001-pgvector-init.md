# 2026-10-05 — VCS-001 pgvector init (subtasks 1 + 9)

- **Skill / agent:** ngoding-backend
- **Ticket / docs refs:** `docs/tasks/p0/VCS-001-domain-schema-persistence.md` (subtasks 1, 9)
- **Stage:** implementation
- **Summary:** Locked vector store to pgvector; switched Compose to `pgvector/pgvector:pg16`; Alembic migration enables `vector` extension and creates `chunk_embeddings` (tenant/bot filters, HNSW cosine, dim 1536); readiness helpers under `infrastructure/vector`.
- **Files:** `docker-compose.yml`, `apps/backend/alembic/versions/001_enable_pgvector.py`, `apps/backend/app/infrastructure/vector/*`, `apps/backend/app/core/settings.py`, `apps/backend/.env.example`, `apps/backend/pyproject.toml`
- **Tests:** `apps/backend/tests/test_vector_store.py`, `test_settings.py`; `uv run pytest`
- **Wiki sync:** `docs/application-spec.md` §12.2, `docs/tasks/README.md`, `docs/tasks/p0/VCS-001-*.md`, `docs/architecture/overview.md`, `docs/architecture/schema.dbml`, `docs/domains/knowledge.md`, `apps/backend/README.md`
- **Open follow-ups:** VCS-001 domain migrations (subtasks 3–8); FK `chunk_embeddings.chunk_id` → `chunks.id`; embedding upsert in VCS-006
