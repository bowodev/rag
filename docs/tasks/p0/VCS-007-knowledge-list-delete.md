# VCS-007 — Knowledge list, status, delete

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `backend` |
| Domains | Knowledge |
| Depends on | VCS-005, VCS-006 |
| Spec refs | application-spec §§5.4, 7, 8 (invariant 6), 9 |

## Goal

Users can list sources with indexing status and delete a source with full cascade of file, chunks, and vectors.

## Scope

### In

- `GET /bots/{id}/sources` (include status)
- `DELETE /bots/{id}/sources/{sourceId}`
- Cascade: remove stored file + chunks + vectors
- Tenant/bot authorization on all routes

### Out

- Reprocess endpoint (nice-to-have / P1)
- Dashboard UI (VCS-010)
- Shared KB across bots

## Acceptance criteria

- [ ] List shows sources with `processing` | `ready` | `failed`
- [ ] Delete removes source so its content is no longer retrievable
- [ ] Delete is scoped: cannot delete another tenant/bot’s source
- [ ] After delete, playground answers no longer use that content (verified with VCS-008/012)
