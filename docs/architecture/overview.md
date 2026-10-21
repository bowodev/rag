# Architecture overview

**Last updated:** 2026-10-21

System shape for Virtuascope VCS. Product scope stays in [`application-spec.md`](../application-spec.md). Backend layering: [`backend.md`](./backend.md).

## Runtime topology

```text
┌────────────────────┐
│  Dashboard (React) │  Virtuascope users (scaffold — not built yet)
└─────────┬──────────┘
          │ Bearer JWT (access) + refresh
          ▼
┌─────────────────────────────────────┐
│ Backend API process (FastAPI)       │
│  auth · me · tenants · knowledge upload │
│  lifespan: RabbitMQ + MinIO bucket      │
└─────────┬───────────────┬───────────┘
          │               │ publish
          │               ▼
          │     ┌─────────────────────┐
          │     │ RabbitMQ            │
          │     │ knowledge.index + DLQ │
          │     └──────────┬──────────┘
          │                │ consume
          │                ▼
          │     ┌─────────────────────┐
          │     │ Consumer process(es)│
          │     │ recovery / DLQ / index │
          │     └──────────┬──────────┘
          ▼                ▼
   ┌──────────────────────────────────┐
   │ Postgres 16 + pgvector           │
   │ domain tables + chunk_embeddings │
   └──────────────────────────────────┘
          ▲
          │ MinIO (S3) raw knowledge files
```

Local infra (`docker compose`): **Postgres (pgvector)**, **RabbitMQ**, **MinIO** (Chainguard free image), optional RabbitScout UI.

## Processes

| Process | Entry | Role |
|---------|-------|------|
| **API** | `uvicorn app.cmd.api.main:app` | Sync HTTP, authz, enqueue jobs, RAG orchestration (when built) |
| **Consumer** | `python -m app.cmd.consumer.main <name>` | Async workers; share domain/application rules with API |

Make targets: `make backend-api`, `make backend-consumer-test`, `make infra-up`.

## Responsibilities

- **API**: request/response, JWT auth, membership checks, enqueue work, playground RAG (P0)
- **Consumers**: async knowledge processing only (and smoke/test handlers today)
- **Postgres**: domain persistence — see [`schema.dbml`](./schema.dbml); bots are metadata-only
- **Backend config**: LLM prompt / model / temperature (RAG in-process; not in Postgres for MVP)
- **Vector store**: pgvector in the same Postgres instance; `chunk_embeddings` filtered by `tenant_id` + `bot_id` (default dim 1536)
- **Queue**: RabbitMQ durable queues via `RabbitMQBus` / consumer registry

## Auth (VCS-002 done; VCS-003 extends)

- Self-hosted **HS256 JWT**: short-lived **access** + longer-lived **refresh**
- `POST /auth/login`, `POST /auth/refresh`, `POST /auth/set-password` (first-time), `GET /me`, `GET /tenants`
- `require_auth` → `AuthContext` (user identity + `platform_role`)
- `require_tenant_membership` → fail-closed on tenant path/body ids
- `require_ops` → `/internal/*` only when `platform_role = ops`
- Details: [`multi-tenancy.md`](./multi-tenancy.md), [`domains/user.md`](../domains/user.md)

## API process lifecycle

On `SIGTERM` / `SIGINT`, uvicorn:

1. Stops accepting new HTTP connections and drains in-flight requests
2. Runs FastAPI lifespan shutdown — close shared deps (e.g. RabbitMQ) **after** HTTP is done

Do not close long-lived deps while requests may still be using them.

## Implemented vs planned (P0)

| Area | Status |
|------|--------|
| Schema + Alembic + pgvector smoke | Done (VCS-001) |
| Auth + `/me` + membership-scoped tenants | Done (VCS-002) |
| Internal user/tenant/membership CRUD + set-password | Done (VCS-003) |
| Knowledge upload + enqueue (+ recovery/DLQ) | Done (VCS-005) |
| Bots read / indexing consumer / chat / dashboard | Planned (VCS-004, VCS-006…) |
| Host chatbot / embed | Deferred (P2) |

Chatbot host integration is **P2** and intentionally omitted from the MVP critical path.
