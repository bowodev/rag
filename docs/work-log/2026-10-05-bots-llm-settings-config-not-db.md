# 2026-10-05 — Bot LLM settings: backend config, not Postgres

- **Skill / agent:** manual / docs
- **Ticket / docs refs:** VCS-001, VCS-008; `docs/architecture/schema.dbml`; `docs/domains/bot.md`
- **Stage:** planning / docs lock
- **Summary:** MVP does not store prompt/model/temperature on `bots`. LLM settings live in backend config; Postgres `bots` is metadata only. Per-tenant prompt editing deferred.
- **Files:** `docs/tasks/p0/VCS-001-domain-schema-persistence.md`, `docs/tasks/p0/VCS-008-playground-chat-rag.md`, `docs/tasks/README.md`, `docs/architecture/schema.dbml`, `docs/architecture/overview.md`, `docs/domains/bot.md`
- **Tests:** n/a
- **Wiki sync:** schema DBML added; tickets/domain aligned
- **Open follow-ups:** vector store choice (pgvector vs Qdrant); later per-tenant/per-bot prompt config when product needs it
