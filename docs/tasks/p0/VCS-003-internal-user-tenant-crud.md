# VCS-003 — Internal User + Tenant CRUD

| Field | Value |
|-------|-------|
| Status | `done` |
| Priority | P0 |
| App | `backend` |
| Domains | Tenant, User |
| Depends on | VCS-001, VCS-002 |
| Spec refs | application-spec §§5.1–5.2, 6, 9 (Auth / Internal) |

## Goal

Provide internal APIs for **User** and **Tenant** CRUD (including membership links) so dashboard users and tenants can be managed. Include self-serve **set password** so users provisioned without a hash can activate login. **No** bot/LLM ops APIs in this ticket.

## Scope

### In

- Internal CRUD + **list/filter** for **Tenant**, **User**, **Membership**
- Protect `/internal/*` with the **same login JWT** as the dashboard; only users with `platform_role = ops`
- Hard delete for tenants, users, and memberships (see rules below)
- User create may leave `password_hash` **null**
- Self-serve `POST /auth/set-password` (first-time set when hash is null)

### Out

- `POST /internal/bots`
- `PATCH /internal/bots/{id}/settings` (or any HTTP API that reads/writes prompt, model, temperature)
- Exposing LLM settings in any response body
- Dashboard UI for ops
- Host onboard (P2)
- Authenticated “change password” when a hash already exists (future; first-time set only here)

## Decisions (locked)

| Topic | Decision |
|-------|----------|
| Ops auth | Same `POST /auth/login` JWT; gate with `require_ops` on `users.platform_role = ops` |
| Platform role | Column `users.platform_role`: `user` \| `ops` (default `user`) |
| Deletes | **Hard delete**. Memberships removed with user/tenant. Tenant/user delete → **409** if other owned resources (e.g. bots) still reference them |
| Password on create | Optional; omit/null → user must call set-password before login |
| Set password | `POST /auth/set-password` `{ email, password }` — succeeds **only** if user exists and `password_hash` is null; otherwise 409 (stable messaging) |
| List/filter | Internal list endpoints with filters (`q`, `status`, `tenant_id`, `user_id` as applicable) |

## Hard rule

Prompt / model / temperature / LLM params are **backend-private**. They must **not** be exposed on internal or public HTTP APIs in P0.

Bots needed for local/MVP demos may be created via seed/fixture or backend-only code paths — not via an ops HTTP API in this phase.

## Acceptance criteria

- [x] Tenant can be created, listed/filtered, read, updated, hard-deleted via internal API
- [x] User can be created, listed/filtered, read, updated, hard-deleted via internal API
- [x] Membership can link a user to a tenant with a role (CRUD + list/filter)
- [x] Non-ops authenticated callers cannot use `/internal/*` (403)
- [x] Unauthenticated callers cannot use `/internal/*` (401)
- [x] User may be created with null `password_hash`
- [x] User with null hash can set password via `POST /auth/set-password`, then login
- [x] Set-password fails if hash already set
- [x] No endpoint in this ticket returns or accepts LLM settings
- [x] Responses never return `password_hash`
