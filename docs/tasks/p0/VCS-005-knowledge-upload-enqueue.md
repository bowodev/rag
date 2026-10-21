# VCS-005 — Knowledge upload + enqueue

| Field | Value |
|-------|-------|
| Status | `done` |
| Priority | P0 |
| App | `backend` |
| Domains | Knowledge |
| Depends on | VCS-004 |
| Spec refs | application-spec §§5.4, 6, 7 (Knowledge), 9 |

## Goal

Authenticated users can upload a knowledge file for a bot; the source is stored and indexing is enqueued with status `processing`.

## Scope

### In

- `POST /bots/{id}/sources` (multipart/file upload)
- Persist Source with `tenant_id`, `bot_id`, status `processing`
- Store raw file in object storage (or agreed MVP storage)
- Enqueue indexing job for consumers
- Membership + bot ownership checks

### Out

- Consumer extract/embed logic (VCS-006)
- Delete / list (VCS-007)
- Reprocess (P1 / VCS-013)
- External connectors

## Acceptance criteria

- [x] Upload creates a Source in `processing`
- [x] Job is enqueued for the new source
- [x] Upload to a bot outside the user’s tenant is denied
- [x] Unsupported / rejected files fail clearly (per decided file types)

## Decisions

- File types: PDF + TXT + DOCX; max 10 MB
- Storage: MinIO (S3 API) via Chainguard free image `cgr.dev/chainguard/minio`
- Cross-tenant / missing bot: HTTP 403
- Publish failure: leave Source `processing`; `knowledge-recovery` republishes; `knowledge-dlq` marks `failed`
- Bot list APIs remain VCS-004; this ticket adds bot repo + ownership check only
