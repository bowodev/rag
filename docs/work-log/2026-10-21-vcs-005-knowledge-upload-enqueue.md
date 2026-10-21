# 2026-10-21 — VCS-005 Knowledge upload + enqueue

## Summary

Implemented `POST /bots/{id}/sources` with MinIO storage, Source `processing`, `IndexSource` enqueue, stuck-source recovery consumer, and DLQ consumer.

## Decisions

- File types: PDF + TXT + DOCX; max 10 MB
- Storage: MinIO via Chainguard free image `cgr.dev/chainguard/minio:latest`
- Cross-tenant / missing bot → 403
- Publish failure → leave `processing`; recovery republishes; DLQ marks `failed`
- GET `/bots` still deferred (VCS-004); bot repo + ownership only

## Verify

- `make infra-up` (includes MinIO on :9000 / console :9001)
- `make backend-test`
- `make backend-consumer-dlq` / `make backend-consumer-recovery`
