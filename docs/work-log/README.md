# Work log

Agents **must** append a work-log entry after implementation stages.

## Location

- Folder: `docs/work-log/`
- File naming: `YYYY-MM-DD-<short-slug>.md`
- Or append to an existing same-day file if closely related

## Entry template

```markdown
# YYYY-MM-DD — <title>

- **Skill / agent:** ngoding-backend | ngoding-dashboard | ngoding-chatbot
- **Ticket / docs refs:** <urls or paths>
- **Stage:** observation | planning | implementation
- **Summary:** what changed and why
- **Files:** key paths
- **Tests:** what was added/run
- **Wiki sync:** which docs updated (or "none — no doc impact")
- **Open follow-ups:** optional
```

## Wiki sync rules

When implementation changes product behavior, agents update the matching wiki page under `docs/` in the same change set:

- Domain rules → `docs/domains/*`
- Flows / tenancy → `docs/architecture/*`
- Scope / acceptance → `docs/application-spec.md` (only with explicit user approval if locking changes)
