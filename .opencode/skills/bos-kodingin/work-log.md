# WORK_LOG.md template (Bos Kodingin)

Create at plan approval / start of Stage 3:

`specs/<id>/WORK_LOG.md`

`<id>` = Linear/GitHub id or kebab-case feature name from Stage 2. Prefer the same directory as `PRODUCT.md` / `TECH.md` when those exist.

The work log is the **handoff artifact** for the next agent/run. Update it whenever you pause or make material progress. It must stay out of git.

## Template

```markdown
# WORK_LOG — <feature name>

**Status:** in_progress | blocked | done
**Current stage:** 3 — Implementation
**Last updated:** YYYY-MM-DD
**Last agent note:** one sentence — what just finished

## Pointers

- Plan / chat summary: …
- Specs: `specs/<id>/PRODUCT.md`, `specs/<id>/TECH.md` (if any)

## Progress

| Task | Status | Notes |
|------|--------|-------|
| … | done | … |
| … | next | … |
| … | pending | … |

## Last completed

**What works now:** …
**Files touched (recent):** …
**How to verify:** …
**Known gaps / follow-ups:** …

## Next for the next agent

**Goal:** …
**Tasks:**
1. …
2. …

**Do not redo:** …
**Blocked on:** none | …

## Decisions since plan approval

- …
```

## Rules for agents

1. **Before starting Stage 3 or resuming:** read `WORK_LOG.md` if it exists; resume from **Next**, do not re-implement completed work.
2. **When pausing or after material progress:** update Status, Progress, Last completed, Next, Last updated.
3. Keep it factual and short — paths, task ids, verify steps. No essay.
4. If the user changes scope mid-flight, note it under Decisions and adjust Next.

## Lifecycle

- **Gitignored** — `specs/**/WORK_LOG.md` must stay out of git (local handoff only).
- **Delete when done** — when Stage 3 acceptance is fully met, **delete** `WORK_LOG.md`. Do not leave a finished work log around.
- Partial / in-progress work keeps the file so the next agent can resume.
