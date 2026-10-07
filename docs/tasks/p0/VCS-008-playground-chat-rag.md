# VCS-008 — Playground chat (RAG)

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `backend` |
| Domains | Chat, Knowledge, Bot |
| Depends on | VCS-004, VCS-006 |
| Spec refs | application-spec §§5.5, 6, 7 (Playground), 8, 9, 10 |

## Goal

Dashboard playground can send a message and receive an answer composed from internal bot settings + retrieved ready knowledge (tenant/bot scoped).

## Scope

### In

- `POST /bots/{id}/chat` (channel = `playground`)
- Persist Conversation + Messages (user + assistant)
- Retrieve chunks filtered by `tenant_id` + `bot_id`, **ready sources only**
- Compose prompt from **backend-private** system settings + context + history
- Call LLM using stored model/params loaded only inside the service layer (never from client input)
- Optional citations on assistant messages
- Empty knowledge: still answer from default prompt **without inventing KB facts**

### Out

- Host chat channel (P2)
- Optional history list endpoints unless needed by UI (`GET` conversations/messages are optional in spec)
- Prompt/model UI
- Returning LLM settings in chat (or any) API responses
- HTTP APIs to create bots or patch settings

## Hard rule

LLM settings are backend-private: read from **backend config** in-process only (not from the `bots` row / request). Do not accept them on the request and do not return them on the response.

## Acceptance criteria

- [ ] Playground answers using relevant knowledge when sources are `ready`
- [ ] Tenant/bot A cannot retrieve Tenant/bot B knowledge
- [ ] Non-`ready` sources never appear in retrieval
- [ ] Empty knowledge does not fabricate KB-specific facts
- [ ] LLM settings come from backend config, not the request body or `bots` columns
- [ ] Chat responses never include prompt/model/temperature fields
