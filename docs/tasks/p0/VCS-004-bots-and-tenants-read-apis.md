# VCS-004 — Bots read APIs (metadata only)

| Field | Value |
|-------|-------|
| Status | `done` |
| Priority | P0 |
| App | `backend` |
| Domains | Bot |
| Depends on | VCS-002 |
| Spec refs | application-spec §§5.3, 6, 9 (Bots) |

## Goal

Dashboard can list provisioned bots for the user’s tenant(s). Responses are **metadata only** — LLM settings are never returned.

## Scope

### In

- `GET /bots` (scoped to current tenant context / membership)
- `GET /bots/{id}` — safe metadata only (e.g. id, name, status, tenant_id)
- Tenant scoping on every read

### Out

- Create/update/delete bot from dashboard or public API
- Any field that reveals prompt, model, temperature, or other LLM params
- Knowledge and chat endpoints (later tickets)
- Internal bot/settings HTTP APIs (deferred)

## Hard rule

Serializers / OpenAPI schemas for these routes must **omit** all LLM settings. Chat uses settings only inside the backend service layer (VCS-008).

## Acceptance criteria

- [x] User only sees bots in their tenant(s)
- [x] Bot detail JSON contains no prompt/model/temperature (or equivalent)
- [x] Accessing another tenant’s bot returns not found / forbidden
- [x] Empty tenant returns empty list (not error)

## Decisions

- `GET /bots` lists bots across **all** membership tenants (no `tenant_id` query)
- Cross-tenant / missing bot → **403** (same as VCS-005 upload)
- All statuses (`draft` / `live` / `disabled`); include `created_at` / `updated_at`
