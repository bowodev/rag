# VCS-019 — Embed / chatbot widget

| Field | Value |
|-------|-------|
| Status | `deferred` |
| Priority | P2 |
| App | `chatbot` |
| Domains | Chat |
| Depends on | VCS-017, VCS-018 |
| Spec refs | application-spec §§1, 6 (Chatbot), 11 |

## Goal

Ship production embed/widget UX in `apps/chatbot` for host integration when needed.

## Scope

### In

- Embeddable chat UI / plugin surface
- Integration against host chat APIs
- Keep scaffold-friendly until P2 starts

### Out

- Replacing dashboard playground
- Any P0 critical-path dependency on this app

## Acceptance criteria

- [ ] Widget can chat against a connected bot
- [ ] Uses host credentials, not dashboard user JWT
- [ ] Does not expand into prompt/model admin UI

## Note

**Out of P0 critical path.** Keep `apps/chatbot` scaffold-only until this ticket is activated.
