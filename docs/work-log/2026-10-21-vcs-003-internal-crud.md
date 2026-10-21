# 2026-10-21 — VCS-003 internal CRUD + set-password

- **Skill / agent:** ngoding-backend
- **Ticket / docs refs:** `docs/tasks/p0/VCS-003-internal-user-tenant-crud.md`, `docs/application-spec.md` v0.5
- **Stage:** implementation
- **Summary:** Added `users.platform_role`, ops-gated `/internal/{tenants,users,memberships}` CRUD + list/filter, hard deletes with membership cascade / 409 on dependents, and first-time `POST /auth/set-password`. Seed now creates an ops user.
- **Files:**
  - `alembic/versions/002_user_platform_role.py`
  - `app/application/{auth/set_password,tenant/ops_crud,user/ops_crud,membership/ops_crud}.py`
  - `app/cmd/api/routes/internal/*`, `routes/auth.py` (set-password)
  - `app/cmd/api/deps/auth.py` (`require_ops`)
  - `scripts/seed_auth_poc.py`
  - tests under `tests/application/*`, `tests/cmd/api/test_internal_routes.py`, `test_require_ops.py`
- **Tests:** `uv run pytest` → 44 passed
- **Wiki sync:** VCS-003 marked done; architecture overview/data-flow status; ticket acceptance checked
- **Open follow-ups:** authenticated change-password when hash already set; wire bots after VCS-004
