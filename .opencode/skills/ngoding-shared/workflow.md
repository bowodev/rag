# Shared coding workflow (VCS)

All `ngoding-*` skills **must** follow these stages in order. Do not skip gates.

## Hard rules (anti-hallucination)

1. Treat attached **docs** and/or **tickets** as the only requirements source of truth.
2. Primary wiki: `docs/` especially `docs/application-spec.md` and `docs/domains/*`.
3. If a detail is missing, ask — do **not** invent product behavior, APIs, or fields.
4. If docs and ticket conflict, stop and ask which wins.
5. Out-of-scope items in the spec (e.g. P2 host connect, prompt UI) must not be implemented unless the user explicitly expands scope.

## Stage 1 — Observation

Goal: align on intent before designing.

Actions:
- Read user request + attached ticket/docs
- Restate: goal, in-scope, out-of-scope, affected domain(s), app (`backend` / `dashboard` / `chatbot`)
- List unknowns / assumptions explicitly
- **Stop and wait** for user confirmation (“OK / proceed”)

If not aligned, continue clarifying in Observation. Do not plan yet.

### Observation output template

```markdown
## Observation
- **Goal:**
- **Sources:** (doc paths / ticket URLs)
- **In scope:**
- **Out of scope:**
- **Affected domains:** Tenant | User | Bot | Knowledge | Chat
- **Target app:**
- **Open questions:**
Awaiting confirmation to enter Planning.
```

## Stage 2 — Planning

Goal: agree on the approach before code.

Actions:
- Describe the solution in product + technical terms
- Provide a **visual diagram**
  - Prefer a **swimlane** (or sequence) diagram for new features / business flows
  - Simpler diagrams are OK for pure refactors/improvements
- Provide **pseudocode in the target language** (Python for backend, TypeScript/React for dashboard/chatbot)
- List files to add/change, tests to add, wiki pages to sync
- **Stop and wait** for user confirmation

If not aligned, revise the plan. Do not implement yet.

### Planning output template

```markdown
## Planning
### Approach
...

### Diagram
```mermaid
...
```

### Pseudocode
...

### File plan
- ...

### Test plan
- ...

### Wiki / work-log sync plan
- ...
Awaiting confirmation to enter Implementation.
```

## Stage 3 — Implementation

Goal: implement exactly what was approved in Planning.

Actions:
1. Implement code changes matching the approved plan
2. Add/update **unit tests** for new behavior
3. Run relevant tests; fix failures you introduced
4. **Auto-sync wiki**: update impacted `docs/**` pages
5. **Auto-sync work log**: add `docs/work-log/YYYY-MM-DD-<slug>.md` (see `docs/work-log/README.md`)
6. Summarize what shipped vs the plan; call out any unavoidable deviations (ask first if scope would change)

## Language

Write skill outputs (observation, planning notes, work logs, wiki updates) in **English**.
