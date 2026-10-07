# Domain: Knowledge

## Purpose

Hold the knowledge a bot may retrieve when answering.

## Core concepts

- Implicit per-bot knowledge scope in MVP (no shared KB entity required)
- **Source**: original input (`file` in MVP)
  - status: `processing` | `ready` | `failed`
- **Chunk**: indexed fragment + vector pointer (internal)
- **Chunk embedding**: pgvector row in `chunk_embeddings` (`tenant_id` + `bot_id` + `chunk_id` + `embedding`)

## Product operations (MVP)

- Upload source
- Delete source
- Observe processing status
- (Optional) reprocess failed source

## System processing (not a domain)

Upload triggers extract → chunk → embed → index. Jobs/queues/retries are application/infrastructure concerns.

## Invariants

- Scoped by `tenant_id` + `bot_id`
- Only `ready` sources are retrievable
- Delete cascades chunks and vectors

## Out of scope

- Prompt/model configuration
- Chat transcripts
- External connectors (P2+)
