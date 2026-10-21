---
name: ngoding-backend
description: >-
  Implements Virtuascope VCS backend work with FastAPI and clean architecture.
  Use when coding apps/backend, APIs, consumers, RAG indexing, multi-tenant
  enforcement, or when the user invokes ngoding-backend.
metadata:
  opencode/slash: "true"
---

# ngoding-backend

Build and change the VCS **backend** (`apps/backend`) using **FastAPI**, clean code, and the locked product docs.

## Mandatory workflow

Follow [../ngoding-shared/workflow.md](../ngoding-shared/workflow.md) stages:

1. **Observation** → wait for user OK  
2. **Planning** (swimlane/sequence + **Python** pseudocode) → wait for user OK  
3. **Implementation** (+ unit tests + wiki + work-log sync)

Do not write production code before Planning is approved.

## Requirements discipline

- Anchor on attached tickets and/or `docs/` (especially `docs/application-spec.md`, `docs/domains/*`, `docs/architecture/*`).
- Do not invent endpoints, fields, or flows absent from those sources.
- Respect MVP locks: no host-connect (P2), no dashboard prompt/model APIs for normal users; settings only via internal/ops paths.

## Stack & layout

- FastAPI + clean layering under `apps/backend/app/` (see `docs/architecture/backend.md`):
  - `cmd/api/` — FastAPI app, routes, deps, errors
  - `cmd/consumer/` — RabbitMQ consumer registry + runner
  - `presenter/` — HTTP / event adapters
  - `middleware/` — auth helpers used by deps
  - `application/` — use-cases, ports, bootstrap services
  - `domain/` — DTOs, auth context, domain errors / invariants
  - `infrastructure/` — DB, JWT, RabbitMQ, vector readiness, (LLM / object storage as added)
  - `config/` — settings from env
- Prefer dependency injection at API boundaries; keep routers thin.
- Domain rules stay in domain/application — not scattered in routers.
- Consumers/workers for knowledge processing stay separate entrypoints but share domain rules.

## Clean code checklist

- Explicit types; avoid `Any`
- Small functions with one reason to change
- Tenant scoping on every query (`tenant_id`, and `bot_id` when bot-owned)
- Fail closed on authz
- Idempotent where the spec requires (e.g. future onboard — do not build early)
- Structured errors; no silent catches

## Testing

- Add unit tests for use-cases and domain rules
- Cover tenant isolation regressions for retrieval/knowledge paths
- Place tests under `apps/backend/tests/`

## Wiki + work log

After implementation:

- Update impacted docs under `docs/`
- Append `docs/work-log/YYYY-MM-DD-<slug>.md`

## Extra reference

- Backend patterns: [reference.md](reference.md)
