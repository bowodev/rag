# Multi-tenancy

**Last updated:** 2026-10-21

## Model (MVP)

Shared database with hard `tenant_id` scoping (row-level isolation by application rules).

## Auth context vs tenant scope

| Concern | Mechanism |
|---------|-----------|
| **Who** is calling | Access JWT → `require_auth` → `AuthContext(user_id, email, platform_role)` |
| **Which** tenants they may use | Memberships; `GET /tenants` lists active membership tenants only |
| **Authorize** a specific tenant | `require_tenant_membership(tenant_id)` → 403 if no membership |
| **Ops / internal APIs** | Same login JWT + `require_ops` (`platform_role = ops`) → else 403 |

Access tokens authenticate **identity** (and carry enough context to enforce ops). They do not embed a selected tenant; tenant authorization is always a membership check.

## Rules

1. Resolve tenant from auth context + membership (dashboard); ops uses `/internal/*` without acting as a tenant member unless they also have membership
2. Every repository/query includes `tenant_id`
3. Bot access implies tenant ownership check
4. Vector queries **must** filter `tenant_id` and `bot_id`
5. Never trust client-supplied tenant ids without membership verification (`require_tenant_membership`)
6. `GET /tenants` is membership-scoped (active tenants only)
7. Wire `require_tenant_membership` into bot / knowledge / chat routes as those APIs land
8. `/internal/*` requires `require_ops`; dashboard JWT with `platform_role=user` is not enough

## Non-goals (MVP)

- Schema-per-tenant
- Physical DB-per-tenant
- Tenant id claimed solely from JWT claims without membership verification
- Separate ops API-key auth (rejected for VCS-003; use login + `ops` role)
