# Virtuascope VCS — OpenCode project instructions

## Build & test

- Infra: `make infra-up` (Postgres + RabbitMQ + MinIO)
- Backend install: `make backend-install`
- Backend API: `make backend-api`
- Backend tests: `make backend-test`
- Consumers: see `make backend-consumer-*`

## Architecture

- Backend layers: `apps/backend/app/{cmd,presenter,middleware,application,domain,infrastructure,config}`
- Architecture KB: `docs/architecture/overview.md`, `docs/architecture/backend.md`
- Locked product spec: `docs/application-spec.md`

## Coding rules

- Follow the shared workflow in `.opencode/skills/ngoding-shared/workflow.md` (Observation → Planning → Implementation; do not skip gates).
- Treat `docs/` and attached tickets as the only requirements source of truth.
- Anchor all work on `docs/application-spec.md` and `docs/domains/*`.
- Tenant scoping on every query (`tenant_id`, and `bot_id` when bot-owned); fail closed on authz.
- Do not implement out-of-scope P2 items (host connect, prompt/model UI) unless explicitly expanded.

## Skills

OpenCode skills live in `.opencode/skills/`:

- `ngoding-backend` — FastAPI clean-architecture backend work
- `ngoding-dashboard` — React dashboard (Virtuascope users)
- `ngoding-chatbot` — React chatbot UI/plugin (P2 host embed)

## Notes

- Migrated from `.cursor/skills/` for OpenCode compatibility.
- `specs/**/WORK_LOG.md` is gitignored handoff state — never commit.
