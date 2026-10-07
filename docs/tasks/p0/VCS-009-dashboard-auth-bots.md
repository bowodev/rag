# VCS-009 — Dashboard auth + bot list

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `dashboard` |
| Domains | User, Tenant, Bot |
| Depends on | VCS-002, VCS-004 |
| Spec refs | application-spec §§6 (Dashboard 1–2, 5), 10 |

## Goal

**Primary dashboard focus:** Virtuascope users can sign in, select/see their tenant context, and list provisioned bots — with **no** prompt/model forms and **no** LLM fields in UI state.

## Scope

### In

- Login / session handling against backend auth
- Tenant context in the UI
- Bot list (and basic bot detail/status from metadata APIs only)
- Navigation shell for Knowledge + Playground routes (stubs OK if those tickets land next)

### Out

- Knowledge upload/delete UI (VCS-010)
- Playground chat UI (VCS-011)
- Any prompt / model / temperature editors or displays
- Ops screens for User/Tenant CRUD (backend internal only)
- Host embed (P2)

## Acceptance criteria

- [ ] User can log in and see only their tenant(s)
- [ ] User sees only bots provisioned for those tenant(s)
- [ ] Dashboard does not expose prompt/model editing
- [ ] Unauthenticated users cannot access bot pages
