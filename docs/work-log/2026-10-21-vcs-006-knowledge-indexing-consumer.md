# 2026-10-21 — VCS-006 Knowledge indexing consumer

## Summary

Implemented `knowledge-index` consumer: download from MinIO → extract (PDF/TXT/DOCX) → chunk → OpenAI embed → replace chunks/`chunk_embeddings` → Source `ready`, or `failed` on error (acked). Ready-only similarity search helper for retrieve gate.

## Decisions

- OpenAI `text-embedding-3-small` (1536)
- Chunk ~1000 chars / 150 overlap
- Catch → session rollback → `mark_failed` → ack
- Idempotent delete-then-rewrite per source
- `SearchReadyChunks` + repo join filters `sources.status = ready`

## Verify

- `make backend-test`
- `make backend-consumer-index` (needs `OPENAI_API_KEY` + infra)
