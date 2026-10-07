# VCS-017 — Host connection & onboard

| Field | Value |
|-------|-------|
| Status | `deferred` |
| Priority | P2 |
| App | `backend` |
| Domains | Bot (connection) |
| Depends on | P0 complete |
| Spec refs | application-spec §11 |

## Goal

Allow a Virtuascope host app (e.g. Photobox) to connect/onboard to a VCS bot with credentials, preserving knowledge on reconnect.

## Scope

### In

- Connection binding `(host_app, external_id)` → one bot
- Onboard API + credentials
- Idempotent onboard; reconnect reuses bot

### Out

- MVP playground work
- Implementing this during P0 unless explicitly requested

## Acceptance criteria

- [ ] Host can onboard and receive connection credentials
- [ ] Reconnect reuses the same bot so knowledge is preserved
- [ ] Binding uniqueness rules from spec §11 are enforced

## Note

**Do not implement in P0.**
