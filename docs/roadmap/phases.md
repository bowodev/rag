# Roadmap phases

## P0 — MVP (current lock)

Outcome: working multi-tenant RAG + **dashboard-first** knowledge management + playground.

- Backend APIs that unblock the dashboard (auth, bots metadata, knowledge, chat)
- Dashboard knowledge upload/delete + playground
- Internal CRUD for **User + Tenant** only
- LLM prompt/model stay **backend-private** (never HTTP-exposed)
- Tenant isolation proven by tests

Out of scope: host connect, production embed, prompt UI, internal bot/LLM settings HTTP APIs.

## P1 — Hardening

- Reprocess failed sources (if not already in P0)
- Retries / DLQ
- Observability
- Rate limits / basic quotas

## P2 — Host integration (low priority)

- Connection/onboarding for apps like Photobox
- Host chat channel + credentials
- Optional embed widget
