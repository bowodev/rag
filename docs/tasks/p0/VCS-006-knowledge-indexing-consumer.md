# VCS-006 — Knowledge indexing consumer

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `backend` |
| Domains | Knowledge |
| Depends on | VCS-001, VCS-005 |
| Spec refs | application-spec §§5.4, 6, 7, 8 (invariants 4–6) |

## Goal

Async consumer processes uploaded sources: extract → chunk → embed → upsert vectors, then mark source `ready` or `failed`.

## Scope

### In

- Consumer pipeline for indexing jobs
- Chunk persistence + vector upsert filtered by `tenant_id` + `bot_id`
- Transition Source status to `ready` on success or `failed` on failure
- Ensure non-`ready` sources never become retrievable

### Out

- Upload HTTP API (VCS-005)
- Delete cascade (VCS-007)
- Retries / DLQ hardening (VCS-014 — P1)
- Reprocess endpoint (VCS-013 — P1)

## Acceptance criteria

- [ ] Successful job ends with Source `ready` and searchable chunks/vectors
- [ ] Failed job ends with Source `failed` (visible to API/UI later)
- [ ] Vectors are stored with `tenant_id` + `bot_id`
- [ ] Sources still `processing` or `failed` are not used in retrieval
