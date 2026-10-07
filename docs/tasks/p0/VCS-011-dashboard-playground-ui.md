# VCS-011 — Dashboard playground UI

| Field | Value |
|-------|-------|
| Status | `todo` |
| Priority | P0 |
| App | `dashboard` |
| Domains | Chat |
| Depends on | VCS-008, VCS-009 |
| Spec refs | application-spec §§6 (Dashboard 4–5), 7, 10 |

## Goal

Provide a playground chat surface so users can test a bot with RAG answers from the dashboard.

## Scope

### In

- Playground chat UI for a selected bot
- Send message → show assistant reply (stream if backend supports it)
- Optional display of citations if returned
- Clear empty-state when bot has no knowledge yet

### Out

- Editing prompt/model from playground
- Production embed widget (`apps/chatbot` — P2)
- Host-app chat UX (P2)

## Acceptance criteria

- [ ] User can send a message and see an answer
- [ ] Answers reflect uploaded ready knowledge when relevant
- [ ] No prompt/model controls appear in the UI
- [ ] Playground is tied to the selected bot / tenant context
