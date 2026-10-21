# VCS-006 — Knowledge indexing consumer

| Field | Value |
|-------|-------|
| Status | `done` |
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

- [x] Successful job ends with Source `ready` and searchable chunks/vectors
- [x] Failed job ends with Source `failed` (visible to API/UI later)
- [x] Vectors are stored with `tenant_id` + `bot_id`
- [x] Sources still `processing` or `failed` are not used in retrieval

## Decisions

- Embeddings: OpenAI `text-embedding-3-small` (dim 1536)
- Chunking: recursive character splitter (~1000 / overlap 150)
- Extract: `pypdf` + `python-docx` + UTF-8 TXT
- Errors: catch → rollback → `mark_failed` → ack (no re-raise)
- Re-delivery: delete prior chunks/embeddings for source, then rewrite
- Ready-only search helper for retrieve gate (VCS-008 reuses)
