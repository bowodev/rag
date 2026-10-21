# VCS-002 — Auth + tenant context

| Field | Value |
|-------|-------|
| Status | `done` |
| Priority | P0 |
| App | `backend` |
| Domains | User, Tenant |
| Depends on | VCS-001 |
| Spec refs | application-spec §§6, 8, 9 (Auth / Tenants) |

## Goal

Dashboard users can authenticate and the API can resolve identity + membership-scoped tenant access.

## Scope

### In

- `POST /auth/login`
- `POST /auth/refresh`
- `GET /me`
- `GET /tenants` (tenants where the user has membership)
- Auth middleware / dependency that rejects unauthenticated requests
- Enforce: users only access tenants where they have membership (invariant 7)
- `require_tenant_membership` dependency for future tenant-scoped routes

### Out

- Bot CRUD for dashboard users
- Prompt/model editing
- Host-app auth / connection tokens (P2)
- Internal user/tenant CRUD (VCS-003)

## Acceptance criteria

- [x] Login returns a usable session/token for subsequent API calls
- [x] `/me` returns the authenticated user
- [x] `/tenants` returns only membership tenants
- [x] Requests without valid auth are rejected
- [x] Cross-tenant access without membership is denied (`require_tenant_membership` → 403)
- [x] Refresh token can mint a new access (+ refresh) pair

## Decisions

- Auth mechanism: **self-hosted JWT** (HS256 access + refresh) — see [spec §12.3](../../application-spec.md)
