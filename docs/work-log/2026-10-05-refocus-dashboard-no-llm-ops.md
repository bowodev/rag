# 2026-10-05 — Refocus backlog: dashboard-first, no bot/LLM ops APIs

- **Skill / agent:** manual / docs
- **Ticket / docs refs:** `docs/tasks/**`, `docs/application-spec.md` (v0.4)
- **Stage:** implementation
- **Summary:** Dropped internal bot/LLM ops from P0. Internal APIs narrowed to User + Tenant CRUD. LLM settings are backend-private and must not be HTTP-exposed. Reordered backlog to prioritize dashboard app.
- **Files:** `docs/tasks/**`, `docs/application-spec.md`, `docs/domains/bot.md`, `docs/roadmap/phases.md`
- **Tests:** n/a
- **Wiki sync:** spec/domain/roadmap aligned with ticket backlog
- **Open follow-ups:** how bots are seeded for local/MVP demos (fixture vs backend-only script)
