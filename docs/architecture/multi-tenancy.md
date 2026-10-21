# Multi-tenancy

## Model (MVP)

Shared database with hard `tenant_id` scoping (row-level isolation by application rules).

## Rules

1. Resolve tenant from auth context (dashboard) or ops input (internal APIs)
2. Every repository/query includes `tenant_id`
3. Bot access implies tenant ownership check
4. Vector queries **must** filter `tenant_id` and `bot_id`
5. Never trust client-supplied tenant ids without membership verification (`require_tenant_membership`)
6. `GET /tenants` is membership-scoped (active tenants only)

## Non-goals (MVP)

- Schema-per-tenant
- Physical DB-per-tenant
