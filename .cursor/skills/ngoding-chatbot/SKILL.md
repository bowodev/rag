---
name: ngoding-chatbot
description: >-
  Implements Virtuascope VCS chatbot UI/plugin with React and official React
  best practices. Use when coding apps/chatbot, embed widget, chat surfaces, or
  when the user invokes ngoding-chatbot.
---

# ngoding-chatbot

Build and change the VCS **chatbot** app (`apps/chatbot`) with **React**, following official React best practices, and the locked product docs.

## Mandatory workflow

Follow [../ngoding-shared/workflow.md](../ngoding-shared/workflow.md) stages:

1. **Observation** → wait for user OK  
2. **Planning** (swimlane/sequence for chat features + **React/TS** pseudocode) → wait for user OK  
3. **Implementation** (+ unit tests + wiki + work-log sync)

Do not write production code before Planning is approved.

## Requirements discipline

- Anchor on attached tickets and/or `docs/`.
- Per locked MVP: host connect / production embed is **P2 (low priority)**.  
  If the user asks for chatbot work during P0, confirm whether this is intentional scope expansion.
- Do not invent auth modes (connection tokens, etc.) unless documented/ticketed.
- Bot prompt/model remain backend concerns — chatbot UI must not expose operator settings editors.

## Official React practices (must follow)

Source of truth: [react.dev](https://react.dev)

1. **Thinking in React** — component hierarchy; minimal state; derive during render.  
   https://react.dev/learn/thinking-in-react
2. **Rules of React** — purity; React owns component/hook calls.  
   https://react.dev/reference/rules
3. **Rules of Hooks** — top-level only.  
   https://react.dev/reference/rules/rules-of-hooks
4. **You Might Not Need an Effect** — avoid Effect-driven React state sync.  
   https://react.dev/learn/you-might-not-need-an-effect
5. **Synchronizing with Effects** — Effects for external systems only (websocket, DOM widget, stream readers), with cleanup.  
   https://react.dev/learn/synchronizing-with-effects

### Chat-specific guidance

- Message list is state; “isScrollingToBottom” etc. should be derived or UI-local, not redundant dual state
- Streaming tokens: treat the network/stream as an external system — Effect or dedicated subscription with cleanup/abort
- Prefer controlled input for composer; send on events, not Effects
- If embedding on third-party pages later: isolate styles (e.g. Shadow DOM) — only when P2/spec says so

## Testing

- Unit-test message state updates, error/empty states, abort/cancel behavior
- Avoid brittle full-stream E2E as the only safety net

## Wiki + work log

After implementation:

- Update impacted `docs/**`
- Append `docs/work-log/YYYY-MM-DD-<slug>.md`

## Extra reference

- [reference.md](reference.md)
