# Multi-tenancy

**Last updated:** 2026-10-21

## Model (MVP)

Shared database with hard `tenant_id` scoping (row-level isolation by application rules).

## Auth context vs tenant scope

| Concern | Mechanism |
|---------|-----------|
| **Who** is calling | Access JWT → `require_auth` → `AuthContext(user_id, email)` |
| **Which** tenants they may use | Memberships; `GET /tenants` lists active membership tenants only |
| **Authorize** a specific tenant | `require_tenant_membership(tenant_id)` → 403 if no membership |

Access tokens authenticate **identity only**. They do not embed a selected tenant; tenant authorization is always a membership check.

## Rules

1. Resolve tenant from auth context + membership (dashboard) or ops input (internal APIs)
2. Every repository/query includes `tenant_id`
3. Bot access implies tenant ownership check
4. Vector queries **must** filter `tenant_id` and `bot_id`
5. Never trust client-supplied tenant ids without membership verification (`require_tenant_membership`)
6. `GET /tenants` is membership-scoped (active tenants only)
7. Wire `require_tenant_membership` into bot / knowledge / chat routes as those APIs land

## Non-goals (MVP)

- Schema-per-tenant
- Physical DB-per-tenant
- Tenant id claimed solely from JWT claims without membership verification
