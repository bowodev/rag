# 2026-10-21 — Architecture KB sync

- **Skill / agent:** general (docs)
- **Ticket / docs refs:** `docs/architecture/*`, `docs/apps/README.md`, `docs/application-spec.md` (auth already locked)
- **Stage:** implementation (documentation only)
- **Summary:** Brought architecture KB in line with the real backend: clean layers (`cmd` / `presenter` / `application` / `domain` / `infrastructure`), JWT auth, RabbitMQ + consumer process, Postgres/pgvector, and current P0 implemented vs planned status.
- **Files:**
  - `docs/architecture/overview.md` (rewrite)
  - `docs/architecture/backend.md` (new)
  - `docs/architecture/data-flow.md` (auth flow + planned markers)
  - `docs/architecture/multi-tenancy.md` (AuthContext vs membership)
  - `docs/architecture/schema.dbml` (password_hash note)
  - `docs/apps/README.md`, `docs/README.md`, `README.md`
  - `.cursor/skills/ngoding-backend/SKILL.md` (layout paths)
- **Tests:** none (docs only)
- **Wiki sync:** architecture + apps index; skill stack paths aligned
- **Open follow-ups:** none
