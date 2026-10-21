# Data flows

**Last updated:** 2026-10-21

## Auth + tenant context (implemented)

```mermaid
sequenceDiagram
  participant U as VCS User
  participant D as Dashboard
  participant API as Backend API
  participant DB as Postgres

  U->>D: Login
  D->>API: POST /auth/login
  API->>DB: Lookup user + verify password_hash
  API-->>D: access_token + refresh_token
  D->>API: GET /me (Bearer access)
  API-->>D: user identity
  D->>API: GET /tenants (Bearer access)
  API->>DB: Memberships for user (active tenants)
  API-->>D: tenant list
  Note over API: Later tenant-scoped routes<br/>use require_tenant_membership
```

Refresh: `POST /auth/refresh` exchanges a valid refresh JWT for a new access (+ refresh) pair.

## Knowledge upload (P0 — planned)

```mermaid
sequenceDiagram
  participant U as VCS User
  participant D as Dashboard
  participant API as Backend API
  participant Q as RabbitMQ
  participant W as Consumer
  participant V as Postgres pgvector

  U->>D: Upload file
  D->>API: POST /bots/{id}/sources
  API->>API: Create Source(processing)
  API->>Q: Enqueue index job
  API-->>D: Source id + status
  Q->>W: Job
  W->>W: Extract / chunk / embed
  W->>V: Upsert vectors (tenant+bot)
  W->>API: Source ready|failed
  D->>API: Poll/list sources
  API-->>D: Status
```

## Playground chat (P0 — planned)

```mermaid
sequenceDiagram
  participant U as VCS User
  participant D as Dashboard
  participant API as Backend API
  participant V as Postgres pgvector
  participant LLM as LLM Provider

  U->>D: Send message
  D->>API: POST /bots/{id}/chat
  API->>API: Persist user message
  API->>V: Retrieve (tenant_id, bot_id)
  V-->>API: Chunks
  API->>LLM: System(internal)+context+history
  LLM-->>API: Answer stream
  API->>API: Persist assistant message
  API-->>D: Answer (+ citations)
```
