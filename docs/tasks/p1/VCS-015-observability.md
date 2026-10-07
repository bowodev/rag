# VCS-015 — Observability

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P1 |
| App | `backend` |
| Domains | — (platform) |
| Depends on | VCS-006, VCS-008 |
| Spec refs | roadmap P1 |

## Goal

Add baseline observability for API and indexing so operators can diagnose tenant-scoped failures.

## Scope

### In

- Structured logging with `tenant_id` / `bot_id` / `source_id` where relevant
- Basic metrics (request latency, job success/failure counts)
- Tracing hooks if already scaffolded in the backend

### Out

- Full product analytics / billing dashboards
- Changing MVP product scope

## Acceptance criteria

- [ ] Failed indexing jobs are diagnosable from logs/metrics
- [ ] Chat and knowledge requests can be correlated by ids
- [ ] No PII beyond what auth already requires is newly exposed in logs without review
