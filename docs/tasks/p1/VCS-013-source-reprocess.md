# VCS-013 — Failed-source reprocess

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P1 |
| App | `backend` (+ optional dashboard) |
| Domains | Knowledge |
| Depends on | VCS-006, VCS-007 |
| Spec refs | application-spec §§9 (`reprocess`), 12.5; roadmap P1 |

## Goal

Allow reprocessing a failed (or selected) source without re-uploading the file.

## Scope

### In

- `POST /bots/{id}/sources/{sourceId}/reprocess`
- Reset status to `processing` and re-enqueue indexing
- Optional dashboard control once API exists

### Out

- New upload path changes
- Host connectors

## Acceptance criteria

- [ ] Reprocess moves source back through indexing
- [ ] Successful reprocess reaches `ready`
- [ ] Unauthorized tenants cannot reprocess others’ sources

## Note

Spec leaves P0 vs P1 open ([§12.5](../../application-spec.md)). This ticket assumes **P1** unless product pulls it into MVP.
