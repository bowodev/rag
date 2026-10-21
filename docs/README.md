# Virtuascope VCS — Knowledge Base

Source of truth for product and engineering decisions for the Virtuascope Chatbot System (VCS).

## How to read

1. [Application Spec (locked)](./application-spec.md) — product scope, domains, MVP
2. [Glossary](./glossary.md) — shared language
3. [Domains](./domains/README.md) — Tenant, User, Bot, Knowledge, Chat
4. [Architecture](./architecture/overview.md) — system shape, processes, auth
   - [Backend layering](./architecture/backend.md)
   - [Data flows](./architecture/data-flow.md)
   - [Multi-tenancy](./architecture/multi-tenancy.md)
   - [Schema (DBML)](./architecture/schema.dbml)
5. [Roadmap](./roadmap/phases.md) — P0 / P1 / P2
6. [Tasks / tickets](./tasks/README.md) — implementation backlog (VCS-001…)
7. [Work log](./work-log/README.md) — implementation diary (agents must sync)

## Apps in this monorepo

| App | Path | Role |
|-----|------|------|
| Backend | `apps/backend` | FastAPI API + knowledge consumers |
| Dashboard | `apps/dashboard` | Virtuascope user console (knowledge + playground) |
| Landing | `apps/landing` | Marketing / entry scaffold |
| Chatbot | `apps/chatbot` | Chat UI / widget (P2; add when scoped) |

Details: [apps/README.md](./apps/README.md).

## Coding skills (Cursor)

Project skills live under `.cursor/skills/`:

- `ngoding-backend`
- `ngoding-dashboard`
- `ngoding-chatbot`

Shared workflow rules: `.cursor/skills/ngoding-shared/workflow.md`

Agents **must** follow attached docs/tickets and must **not** invent requirements outside those sources.
