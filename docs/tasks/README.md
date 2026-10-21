# VCS task backlog

Tickets derived from the [Application Spec](../application-spec.md) (v0.4).

## How to use

1. Pick the next **todo** ticket in dependency order (see Recommended order).
2. Agents follow `.cursor/skills/ngoding-shared/workflow.md` (Observation → Planning → Implementation).
3. Ticket + `docs/application-spec.md` (+ domain docs) are the **only** requirements sources — do not invent scope.
4. When done: set `Status` to `done`, sync wiki/work-log as required by the skill.

## Current focus

**Dashboard app first.** Backend work in P0 exists to unblock dashboard auth, bots list, knowledge, and playground.

| Do now | Do not do now |
|--------|----------------|
| Dashboard UI + its supporting APIs | Internal bot / LLM ops HTTP APIs |
| Internal CRUD for **User + Tenant** only | Exposing prompt / model / temperature anywhere |
| Bot metadata reads for the dashboard | Host connect / embed (P2) |

LLM prompt/model/params live **only inside backend config** (loaded in-process by RAG). They are **never** stored on `bots` in MVP and **never** exposed via API or dashboard.

## Status legend

| Status | Meaning |
|--------|---------|
| `todo` | Not started |
| `in_progress` | Actively being implemented |
| `blocked` | Waiting on decision or dependency |
| `done` | Shipped + acceptance checked |
| `deferred` | Explicitly postponed |

## Recommended order (P0)

```text
VCS-001 schema (bots = metadata only; LLM settings in backend config)
   └─ VCS-002 auth
         ├─ VCS-003 internal User + Tenant CRUD
         └─ VCS-004 bots read APIs (metadata only)
               │
               ├─ VCS-009 dashboard shell (auth + bots)   ← PRIMARY FOCUS
               │     ├─ VCS-010 knowledge UI   ← needs VCS-005…007
               │     └─ VCS-011 playground UI  ← needs VCS-008
               │
               ├─ VCS-005 knowledge upload
               │     └─ VCS-006 indexing consumer
               │           └─ VCS-007 list/delete (+ cascade)
               └─ VCS-008 playground chat API
                     └─ VCS-012 isolation / acceptance
```

## Index

### P0 — MVP (dashboard-first)

| ID | Title | App | Status |
|----|-------|-----|--------|
| [VCS-001](./p0/VCS-001-domain-schema-persistence.md) | Domain schema & persistence | backend | done |
| [VCS-002](./p0/VCS-002-auth-and-tenant-context.md) | Auth + tenant context | backend | done |
| [VCS-003](./p0/VCS-003-internal-user-tenant-crud.md) | Internal User + Tenant CRUD | backend | done |
| [VCS-004](./p0/VCS-004-bots-and-tenants-read-apis.md) | Bots read APIs (metadata only) | backend | todo |
| [VCS-005](./p0/VCS-005-knowledge-upload-enqueue.md) | Knowledge upload + enqueue | backend | todo |
| [VCS-006](./p0/VCS-006-knowledge-indexing-consumer.md) | Knowledge indexing consumer | backend | todo |
| [VCS-007](./p0/VCS-007-knowledge-list-delete.md) | Knowledge list, status, delete | backend | todo |
| [VCS-008](./p0/VCS-008-playground-chat-rag.md) | Playground chat (RAG) | backend | todo |
| [VCS-009](./p0/VCS-009-dashboard-auth-bots.md) | Dashboard auth + bot list | dashboard | todo |
| [VCS-010](./p0/VCS-010-dashboard-knowledge-ui.md) | Dashboard knowledge UI | dashboard | todo |
| [VCS-011](./p0/VCS-011-dashboard-playground-ui.md) | Dashboard playground UI | dashboard | todo |
| [VCS-012](./p0/VCS-012-tenant-isolation-acceptance.md) | Tenant isolation & MVP acceptance | backend + dashboard | todo |

### P1 — Hardening

| ID | Title | App | Status |
|----|-------|-----|--------|
| [VCS-013](./p1/VCS-013-source-reprocess.md) | Failed-source reprocess | backend | todo |
| [VCS-014](./p1/VCS-014-consumer-retries-dlq.md) | Consumer retries / DLQ | backend | todo |
| [VCS-015](./p1/VCS-015-observability.md) | Observability | backend | todo |
| [VCS-016](./p1/VCS-016-rate-limits-quotas.md) | Rate limits / basic quotas | backend | todo |

### P2 — Later (do not start in MVP)

| ID | Title | App | Status |
|----|-------|-----|--------|
| [VCS-017](./p2/VCS-017-host-connection-onboard.md) | Host connection & onboard | backend | deferred |
| [VCS-018](./p2/VCS-018-host-chat-channel.md) | Host chat channel | backend | deferred |
| [VCS-019](./p2/VCS-019-embed-widget.md) | Embed / chatbot widget | chatbot | deferred |

### Explicitly deferred (not in current P0)

| Item | Notes |
|------|--------|
| Internal bot create / LLM settings HTTP APIs | LLM stays backend-private; no ops HTTP for bots/settings in this phase |
| Prompt/model UI | Non-goal permanently for dashboard MVP |

## Open decisions (blockers to clarify)

From [application-spec §12](../application-spec.md):

1. MVP file types: PDF + TXT, or also DOCX?
2. ~~Vector store: pgvector (proposed) vs Qdrant~~ **Resolved:** pgvector
3. Dashboard auth: managed vs self-hosted JWT
4. ~~Bot creation / settings API shape~~ → **Resolved:** no HTTP exposure of LLM settings; bot rows via seed/backend-only for now; internal APIs = User + Tenant CRUD only
5. Failed-source reprocess: P0 or P1? (tickets assume **P1** unless decided otherwise)
