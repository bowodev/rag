# VCS-003 — Internal User + Tenant CRUD

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `backend` |
| Domains | Tenant, User |
| Depends on | VCS-001, VCS-002 |
| Spec refs | application-spec §§5.1–5.2, 6, 9 (Internal) |

## Goal

Provide internal APIs for **User** and **Tenant** CRUD (including membership links) so dashboard users and tenants can be managed. **No** bot/LLM ops APIs in this ticket.

## Scope

### In

- Internal CRUD for **Tenant**
- Internal CRUD for **User**
- Membership create/update/delete (user ↔ tenant + role) as part of that surface
- Protect internal routes (ops-only auth — mechanism agreed in planning)

### Out

- `POST /internal/bots`
- `PATCH /internal/bots/{id}/settings` (or any HTTP API that reads/writes prompt, model, temperature)
- Exposing LLM settings in any response body
- Dashboard UI for ops
- Host onboard (P2)

## Hard rule

Prompt / model / temperature / LLM params are **backend-private**. They must **not** be exposed on internal or public HTTP APIs in P0.

Bots needed for local/MVP demos may be created via seed/fixture or backend-only code paths — not via an ops HTTP API in this phase.

## Acceptance criteria

- [ ] Tenant can be created, read, updated, deleted via internal API
- [ ] User can be created, read, updated, deleted via internal API
- [ ] Membership can link a user to a tenant with a role
- [ ] No endpoint in this ticket returns or accepts LLM settings
- [ ] Non-ops callers cannot use internal endpoints
