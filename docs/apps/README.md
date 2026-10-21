# Apps notes

See locked responsibilities in [Application Spec](../application-spec.md).  
Backend layering: [architecture/backend.md](../architecture/backend.md).

| App | Path | MVP focus | Status |
|-----|------|-----------|--------|
| `backend` | `apps/backend` | API, consumers, tenancy, RAG, private bot settings | Active — auth + schema in place |
| `dashboard` | `apps/dashboard` | Knowledge upload/delete, bot list, playground | Scaffold (empty) |
| `landing` | `apps/landing` | Marketing / entry (non-MVP) | Scaffold (empty) |
| `chatbot` | `apps/chatbot` | Host embed / widget | Deferred (P2); path may be added when scoped |

## Backend stack (current)

- FastAPI + uvicorn
- SQLAlchemy async + Alembic
- Postgres 16 + pgvector
- RabbitMQ (`aio_pika`) + consumer registry
- Self-hosted HS256 JWT (access + refresh)

Local: `make infra-up`, `make backend-api`, `make backend-test`.
