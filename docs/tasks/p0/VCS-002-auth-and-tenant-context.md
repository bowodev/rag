# VCS-002 — Auth + tenant context

| Field | Value |
|-------|-------|
| Status | `todo` |
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
- `GET /me`
- `GET /tenants` (tenants where the user has membership)
- Auth middleware / dependency that rejects unauthenticated requests
- Enforce: users only access tenants where they have membership (invariant 7)

### Out

- Bot CRUD for dashboard users
- Prompt/model editing
- Host-app auth / connection tokens (P2)

## Acceptance criteria

- [ ] Login returns a usable session/token for subsequent API calls
- [ ] `/me` returns the authenticated user
- [ ] `/tenants` returns only membership tenants
- [ ] Requests without valid auth are rejected
- [ ] Cross-tenant access without membership is denied

## Open decisions

- Auth mechanism: managed vs self-hosted JWT ([spec §12.3](../../application-spec.md))
