# VCS-016 — Rate limits / basic quotas

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P1 |
| App | `backend` |
| Domains | Tenant, Knowledge, Chat |
| Depends on | VCS-005, VCS-008 |
| Spec refs | roadmap P1; non-goals still exclude billing |

## Goal

Protect the platform with basic per-tenant rate limits / quotas on upload and chat.

## Scope

### In

- Rate limiting on `POST` knowledge upload and playground chat
- Sensible default limits (document chosen values)
- Clear 429 / quota error responses

### Out

- Billing, plans, payment
- Complex quota UI

## Acceptance criteria

- [ ] Excess upload/chat traffic is throttled per tenant (or agreed key)
- [ ] Legitimate MVP usage remains usable under defaults
- [ ] Limits are documented for operators
