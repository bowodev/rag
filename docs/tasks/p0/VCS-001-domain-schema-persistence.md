# VCS-001 — Domain schema & persistence

| Field | Value |
|-------|-------|
| Status | `done` |
| Priority | P0 |
| App | `backend` |
| Domains | Tenant, User, Bot, Knowledge, Chat |
| Depends on | — |
| Spec refs | application-spec §§5, 8; domains/*; architecture/schema.dbml |

## Goal

Establish Postgres (and vector store) persistence for MVP domains with `tenant_id` / `bot_id` scoping baked into the schema.

## Scope

### In

- Tables / models for: Tenant, User, Membership (role), Bot (**metadata only**), Source, Chunk, Conversation, Message
- Migrations aligned with [`docs/architecture/schema.dbml`](../../architecture/schema.dbml)
- Vector storage choice implementation for chunk embeddings (see open decision)
- Unique / FK constraints that enforce bot→tenant ownership

### Out

- Public HTTP APIs (later tickets)
- Indexing consumer logic
- Dashboard UI
- Host connect (P2)
- Bot LLM settings columns (`system_prompt`, `model`, `temperature`, etc.) — **not in Postgres for MVP**
- Any HTTP exposure of bot LLM settings (never — even “internal ops”)
- Per-tenant / per-bot prompt editing (future; not MVP)

## Hard rule

MVP LLM settings (prompt / model / temperature) live in **backend config** (env / YAML / settings module), loaded in-process by the RAG layer. They are **not** stored on the `bots` table and must never appear in any API contract.

`bots` persists identity + status metadata only (`id`, `tenant_id`, `name`, `status`, timestamps).

## Subtasks

1. **Lock vector store choice** — ~~decide pgvector vs Qdrant~~ **done: pgvector**
2. **DB tooling** — ~~Postgres wiring + migration tool (e.g. Alembic) on empty DB~~ **done**
3. **Enums + base models** — ~~shared types / timestamps; no LLM settings on bots~~ **done** (`app/infrastructure/database/enum.py`, `base.py`)
4. **Identity tables** — ~~`tenants`, `users`, `memberships` (+ unique `tenant_id+user_id`)~~ **done**
5. **Bot metadata table** — ~~`bots` (`id`, `tenant_id`, `name`, `status` only)~~ **done**
6. **Knowledge tables** — ~~`sources`, `chunks` (`tenant_id` + `bot_id`, source status enum, `vector_id` pointer)~~ **done**
7. **Chat tables** — ~~`conversations`, `messages` (+ optional `citations` jsonb)~~ **done**
8. **Constraints / indexes** — ~~FK ownership bot→tenant; indexes for tenant/bot scoped queries~~ **done**
9. **Vector store init** — ~~pgvector extension + `chunk_embeddings` with `tenant_id` + `bot_id`~~ **done** (FK `chunk_id` → `chunks.id` in migration `001`)
10. **Smoke verify** — ~~migrations apply cleanly; models import; vector store reachable (no APIs yet)~~ **done** (`alembic upgrade head`, `tests/test_vcs001_smoke.py`)

## Acceptance criteria

- [x] Schema covers all MVP domain entities from the spec / DBML
- [x] Every tenant-owned row can be filtered by `tenant_id`
- [x] Knowledge and Chat rows are owned via `bot_id` (bot owned by tenant)
- [x] `bots` has **no** LLM settings columns
- [x] Source status enum supports `processing` | `ready` | `failed`
- [x] Migrations apply cleanly on empty DB
- [x] Vector store is initialized and ready for later upsert (VCS-006)

## Open decisions

- ~~Vector store: pgvector vs Qdrant~~ **Resolved:** pgvector ([spec §12.2](../../application-spec.md))
