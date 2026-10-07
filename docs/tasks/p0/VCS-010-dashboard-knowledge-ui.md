# VCS-010 — Dashboard knowledge UI

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `dashboard` |
| Domains | Knowledge |
| Depends on | VCS-007, VCS-009 |
| Spec refs | application-spec §§6 (Dashboard 3), 7, 10 |

## Goal

Per-bot knowledge management in the dashboard: upload, delete, and clear indexing status.

## Scope

### In

- Sources list with status (`processing` | `ready` | `failed`)
- Upload file flow
- Delete source flow (with confirmation appropriate to destructive action)
- Polling or refresh so status updates are visible after indexing

### Out

- Reprocess button (unless reprocess is pulled into P0)
- Shared KB across bots
- External connectors
- Prompt/model UI

## Acceptance criteria

- [ ] Upload shows source entering `processing` then `ready` or `failed`
- [ ] Delete removes the source from the list
- [ ] User cannot manage knowledge for bots outside their tenant
- [ ] Failed status is visible (not a silent failure)
