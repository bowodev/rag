# Virtuascope VCS

Multi-tenant RAG chatbot platform for the Virtuascope ecosystem.

## Apps

| App | Path | Notes |
|-----|------|--------|
| Backend | `apps/backend` | FastAPI API + RabbitMQ consumers |
| Dashboard | `apps/dashboard` | React (Virtuascope users) — scaffold |
| Landing | `apps/landing` | Scaffold |
| Chatbot | `apps/chatbot` | P2 host embed — deferred |

Architecture KB: [`docs/architecture/overview.md`](./docs/architecture/overview.md), backend layers: [`docs/architecture/backend.md`](./docs/architecture/backend.md).

## Local infrastructure

Postgres (**pgvector**) + RabbitMQ via Compose:

```bash
make infra-up
# or: docker compose up -d
```

See [`apps/backend/README.md`](./apps/backend/README.md) for connection URL and migrations.

## Knowledge base

Start here: [`docs/README.md`](./docs/README.md)

Locked product spec: [`docs/application-spec.md`](./docs/application-spec.md)

## Cursor skills

- `ngoding-backend`
- `ngoding-dashboard`
- `ngoding-chatbot`

Shared workflow: `.cursor/skills/ngoding-shared/workflow.md` (Observation → Planning → Implementation).
