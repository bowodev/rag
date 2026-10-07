# VCS-014 — Consumer retries / DLQ

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P1 |
| App | `backend` |
| Domains | Knowledge |
| Depends on | VCS-006 |
| Spec refs | roadmap P1; application-spec §5.4 (system processing) |

## Goal

Make indexing resilient: retries for transient failures and a dead-letter path for poison messages.

## Scope

### In

- Retry policy for consumer jobs
- DLQ / failed-job visibility for ops
- Ensure Source ends in `failed` when retries exhausted

### Out

- Product analytics
- Changing core RAG chat behavior

## Acceptance criteria

- [ ] Transient failures retry without manual re-upload
- [ ] Exhausted retries leave a clear `failed` source state
- [ ] Poison messages do not block the main queue indefinitely
