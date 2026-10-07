# VCS-018 — Host chat channel

| Field | Value |
|-------|-------|
| Status | `deferred` |
| Priority | P2 |
| App | `backend` |
| Domains | Chat |
| Depends on | VCS-017 |
| Spec refs | application-spec §11 |

## Goal

Serve chat for host-app end users via a host channel authenticated with connection tokens (not dashboard JWT).

## Scope

### In

- Host chat channel distinct from `playground`
- Auth via connection token
- Tenant/bot isolation unchanged

### Out

- Dashboard playground changes beyond what’s needed to keep channels separate
- P0 work

## Acceptance criteria

- [ ] Host messages use connection-token auth
- [ ] Host channel cannot access another bot’s knowledge
- [ ] Playground and host conversations remain distinguishable by channel

## Note

**Do not implement in P0.**
