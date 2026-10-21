---
name: ngoding-dashboard
description: >-
  Implements Virtuascope VCS dashboard app with React and official React best
  practices. Use when coding apps/dashboard, knowledge UI, playground chat, or
  when the user invokes ngoding-dashboard.
metadata:
  opencode/slash: "true"
---

# ngoding-dashboard

Build and change the VCS **dashboard** (`apps/dashboard`) with **React**, following official React best practices, and the locked product docs.

## Mandatory workflow

Follow [../ngoding-shared/workflow.md](../ngoding-shared/workflow.md) stages:

1. **Observation** → wait for user OK  
2. **Planning** (swimlane/sequence for features + **React/TS** pseudocode) → wait for user OK  
3. **Implementation** (+ unit tests + wiki + work-log sync)

Do not write production code before Planning is approved.

## Requirements discipline

- Anchor on attached tickets and/or `docs/` (especially `docs/application-spec.md`).
- Dashboard is for **Virtuascope users**: list bots, **upload/delete knowledge**, playground chat.
- **Never** add UI to edit bot prompt/model/temperature (backend/ops only).
- Do not build Photobox connect/onboarding unless scope is explicitly expanded to P2.

## Official React practices (must follow)

Source of truth: [react.dev](https://react.dev)

1. **Thinking in React** — break UI into components; keep **minimal state**; derive the rest during render; one-way data flow.  
   https://react.dev/learn/thinking-in-react
2. **Rules of React** — components/hooks pure; React calls components/hooks; follow Rules of Hooks.  
   https://react.dev/reference/rules
3. **Rules of Hooks** — top level only; only from React functions/custom hooks.  
   https://react.dev/reference/rules/rules-of-hooks
4. **You Might Not Need an Effect** — do not sync React state with Effects; calculate during render; put user-triggered logic in event handlers.  
   https://react.dev/learn/you-might-not-need-an-effect
5. **Effects** — only to sync with **external** systems; declare dependencies honestly; clean up.  
   https://react.dev/learn/synchronizing-with-effects

### Practical rules for this app

- Prefer server state via the project’s data library (TanStack Query when present) over `useEffect` fetching
- Zustand (if used) only for client UI state — never API entity caches
- Forms: React Hook Form + Zod when forms exist
- Keep components pure; no side effects during render

## MVP screens (from spec)

1. Auth + tenant context  
2. Bot list (read-only settings)  
3. Knowledge: upload, delete, status  
4. Playground chat  

## Testing

- Unit-test components/hooks for state transitions and error UI
- Cover knowledge upload/delete happy paths and failure rendering where practical

## Wiki + work log

After implementation:

- Update impacted `docs/**`
- Append `docs/work-log/YYYY-MM-DD-<slug>.md`

## Extra reference

- [reference.md](reference.md)
