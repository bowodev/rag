# Architecture overview

```text
┌────────────────────┐
│  Dashboard (React) │  Virtuascope users
└─────────┬──────────┘
          │ JWT / session
          ▼
┌─────────────────────────────────────┐
│ Backend API (FastAPI)               │
│  auth · bots · knowledge · chat     │
└─────────┬───────────────┬───────────┘
          │               │ enqueue
          │               ▼
          │     ┌─────────────────────┐
          │     │ Queue + Consumers   │
          │     │ extract→embed→index │
          │     └──────────┬──────────┘
          ▼                ▼
   ┌──────────────────────────────────┐
   │ Postgres (pgvector)              │
   │ domains + chunk_embeddings       │
   └──────────────────────────────────┘
          ▲
          │ object storage for raw files
```

## Responsibilities

- **API**: synchronous request/response, authz, enqueue work, RAG chat orchestration
- **Consumers**: async knowledge processing only
- **Postgres**: domain persistence (see [`schema.dbml`](./schema.dbml); bots are metadata-only)
- **Backend config**: LLM prompt / model / temperature (RAG in-process; not in Postgres for MVP)
- **Vector store**: pgvector in the same Postgres instance; `chunk_embeddings` filtered by `tenant_id` + `bot_id` (default dim 1536)

Chatbot host integration is **P2** and intentionally omitted from the MVP critical path.
