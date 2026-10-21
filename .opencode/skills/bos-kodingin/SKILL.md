---
name: bos-kodingin
description: >-
  Three-stage gated delivery: exploration → planning (pseudocode/sketches +
  swimlane) → implementation with a gitignored WORK_LOG handoff file. Never
  advance a stage without explicit user confirmation. Use when the user says
  bos-kodingin, /bos-kodingin, kodingin, or asks to explore-then-plan-then-
  implement with approval gates between stages.
disable-model-invocation: true
metadata:
  opencode/slash: "true"
---

# Bos Kodingin

Structured delivery with **hard stage gates**. Similar spirit to spec-driven work, but the user must confirm before every advance.

| Stage | Name | Stop condition |
|-------|------|----------------|
| 1 | Exploration | User confirms the problem understanding |
| 2 | Planning | User approves the plan (or requests revisions) |
| 3 | Implementation | Acceptance criteria met; stop |

**Never skip stages. Never write application code in Stage 1 or 2. Never enter the next stage without an explicit user go-ahead** (e.g. "lanjut", "ok", "setuju", "approve", "go", or clear corrections that also grant proceed).

If the user only wants one stage (e.g. "explore dulu"), stay in that stage and wait.

## Progress checklist

Copy and keep updated in the reply:

```
Bos Kodingin:
- [ ] Stage 1: Exploration — understood + user confirmed
- [ ] Stage 2: Planning — plan + swimlane + user approved
- [ ] Stage 3: Implementation — done + verified (+ WORK_LOG deleted)
```

## Repo grounding (all stages)

Before planning or implementing, load whatever the current repo already uses:

1. `AGENTS.md`, `docs/kb/`, `.opencode/skills/`, `.cursor/skills/`, `.cursor/rules/` when present
2. Nearest existing patterns for the layers you will touch
3. Prefer additive changes that match local structure — do not reorganize unless asked

During Stage 3, follow those rules as the source of truth for how to code in that repo.

Optional: if the change is substantial and the repo already uses `specs/<id>/PRODUCT.md` + `TECH.md` (or the user asks for specs), write or update those **during Stage 2** as part of the plan artifacts — still no implementation until Stage 2 is approved.

---

## Stage 1: Exploration

**Goal:** Understand what the user wants — dig deep. Not how to build it yet.

### Do

1. Restate the request in your own words (goal, actors, success).
2. Clarify ambiguity aggressively: ask concrete questions; do not invent product intent.
3. Identify **in scope** vs **out of scope**.
4. Read-only scan of relevant entrypoints, APIs, models, UI surfaces. Cite concrete paths.
5. Surface assumptions, risks, and unknowns as explicit questions.
6. Keep digging until the request is unambiguous enough to plan — prefer one more clarifying question over a guessed requirement.

### Do not

- Write implementation plans, pseudocode, or diagrams yet.
- Edit application code, configs, or migrations.
- Invent APIs, schema, or UX without checking what already exists (or asking).

### Output template

```markdown
## Exploration

**Request (restated):** …
**Success looks like:** …
**Actors / surfaces:** …
**In scope:** …
**Out of scope:** …
**Relevant existing pieces:** `path` — why
**Assumptions:** …
**Risks / constraints:** …
**Open questions:** …

Confirm this understanding (or correct it) before I move to Planning.
```

**Gate:** Wait for user confirmation or corrections. Only then enter Stage 2.

---

## Stage 2: Planning

**Goal:** Make the work reviewable before any patches. Prefer diagrams; **recommend a swimlane**.

### Do

1. Re-read Stage 1 confirmation; do not expand scope silently.
2. Break work into ordered tasks (smallest coherent slices).
3. Include:
   - Pseudocode and/or sketch code in the **languages/stack the repo actually uses**
   - File / layer touch list following existing layering
   - At least one **swimlane** (Mermaid `sequenceDiagram`, swimlanes.io-style) — see [swimlane.md](swimlane.md)
   - Acceptance checks + explicit non-goals
4. Call out migrations, config, auth, contracts, and cross-service impact early.
5. If useful for this repo/user, draft `PRODUCT.md` / `TECH.md` under `specs/<id>/` as plan artifacts (still no feature code).
6. Name the feature `<id>` (ticket or kebab-case) and state where `specs/<id>/WORK_LOG.md` will live — create the scaffold **when Stage 2 is approved** (or at the start of Stage 3) so later agents can hand off. Format: [work-log.md](work-log.md).

### Do not

- Implement or apply patches to product code.
- Expand beyond confirmed Exploration without asking.
- Skip the swimlane when the flow has more than one actor/system.

### Output template

```markdown
## Plan

**Summary:** …
**Stack / areas:** …
**Non-goals:** …

### Swimlane
[mermaid sequenceDiagram — see swimlane.md]

### Tasks
1. …
2. …

### Sketches
- Pseudocode / signatures / illustrative snippets in repo languages …

### Acceptance
- [ ] …

**Work log path:** `specs/<id>/WORK_LOG.md`

Approve this plan (or say what to change) before I implement.
```

**Gate:** Wait for approval. Revise if asked. Do not enter Stage 3 without approval.

---

## Stage 3: Implementation

**Goal:** Implement exactly the approved plan, using the repo’s rules and patterns for the areas you touch.

### Work log handoff

Maintain gitignored `specs/<id>/WORK_LOG.md` (see [work-log.md](work-log.md)):

1. **Read** it before starting (or create from the template if missing).
2. **Update** it as progress lands — what is done, what is next, how to verify, blockers — so another agent can resume.
3. **Delete** it when Stage 3 is fully finished (acceptance met or user accepts a documented gap). Never leave a finished work log in the tree.
4. Never commit it — `specs/**/WORK_LOG.md` is gitignored.

### Do

1. Read `specs/<id>/WORK_LOG.md` if present (else create from [work-log.md](work-log.md)); resume from last state — do not redo completed work.
2. Re-read approved plan + relevant project rules/skills.
3. Implement task-by-task; match naming, layering, errors, and test style already in the repo.
4. Keep diffs focused — no drive-by refactors or unplanned dependencies.
5. Run focused verification called out in the plan.
6. Keep WORK_LOG current while work is in flight; report what changed and how to verify.
7. If behavior drifts from the approved plan or checked-in specs, update those artifacts in the same change set when the repo uses them.
8. When fully done: satisfy acceptance, then **delete** `WORK_LOG.md`.

### Do not

- Re-open exploration or redesign unless the user explicitly changes direction.
- Add “flexibility”, providers, or polish not in the approved plan.
- Stop mid-flight without updating WORK_LOG (other agents need last state).
- Commit `WORK_LOG.md` (gitignored; handoff only).
- Leave WORK_LOG around after the feature is fully done — **delete it** on completion.
- Commit or open a PR unless the user asks.

### Done when

The Stage 2 acceptance checklist is satisfied (or the user accepts a documented gap), and `specs/<id>/WORK_LOG.md` has been deleted.

---

## Stage transitions (cheat sheet)

| User says (examples) | You do |
|----------------------|--------|
| Starts with request / "bos-kodingin …" | Stage 1 only; end with confirm ask |
| "ok", "benar", "lanjut planning" | Stage 2 |
| "revisi plan: …" | Stay Stage 2; revise; ask again |
| "approve", "gas implement", "lanjut" | Stage 3 — implement approved plan; keep WORK_LOG updated |
| Pause / handoff mid-implement | Update WORK_LOG with last state before stopping |
| Mid-implement scope change | Pause; return to Stage 1 or 2 as needed; note in WORK_LOG; re-gate |
| Feature fully done | Delete WORK_LOG |

## Related

- Swimlane format: [swimlane.md](swimlane.md)
- Work log handoff: [work-log.md](work-log.md)
- When the user also wants checked-in product/tech specs, compose with `spec-driven-implementation` / `write-product-spec` **inside Stage 2**, still gated before Stage 3.
