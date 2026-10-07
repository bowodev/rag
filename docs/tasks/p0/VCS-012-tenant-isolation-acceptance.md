# VCS-012 — Tenant isolation & MVP acceptance

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `backend` + `dashboard` |
| Domains | Tenant, Bot, Knowledge, Chat |
| Depends on | VCS-003 … VCS-011 |
| Spec refs | application-spec §§8, 10 |

## Goal

Prove P0 acceptance end-to-end — especially multi-tenant isolation and the rule that LLM settings are **never exposed** (API or dashboard).

## Scope

### In

- Automated tests (preferred) and/or documented manual checklist covering §10
- Cross-tenant retrieval negative tests (vector + API)
- Delete-impact test: deleted knowledge no longer affects answers
- Empty-knowledge behavior check
- Confirm dashboard has no prompt/model edit (or display) surfaces
- Confirm public + internal HTTP responses omit LLM settings

### Out

- P1 hardening features
- P2 host connect
- Internal bot/settings HTTP APIs

## Acceptance criteria (spec §10)

- [ ] Internal path can CRUD users + tenants (and memberships)
- [ ] Dashboard user only sees bots in their tenant(s)
- [ ] Upload file → status becomes `ready` (or visible `failed`)
- [ ] Delete file → content no longer used in answers
- [ ] Playground answers using relevant knowledge context
- [ ] Tenant/bot A cannot retrieve Tenant/bot B knowledge
- [ ] Dashboard does not expose prompt/model editing (or LLM fields)
- [ ] No HTTP API returns or accepts bot LLM settings
- [ ] Empty knowledge: bot can still answer from default prompt without inventing KB facts
