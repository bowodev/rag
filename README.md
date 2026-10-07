# Virtuascope VCS

Multi-tenant RAG chatbot platform for the Virtuascope ecosystem.

## Apps

| App | Path | Notes |
|-----|------|--------|
| Backend | `apps/backend` | FastAPI |
| Dashboard | `apps/dashboard` | React (Virtuascope users) |
| Chatbot | `apps/chatbot` | React (P2 priority for host embed) |

## Local infrastructure

Postgres + **pgvector** for backend development (`pgvector/pgvector:pg16`):

```bash
docker compose up -d postgres
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
