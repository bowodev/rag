# 2026-10-20 — API graceful shutdown

- **Skill / agent:** ngoding-backend
- **Ticket / docs refs:** user request; `docs/architecture/overview.md`
- **Stage:** implementation
- **Summary:** Added FastAPI lifespan for shared RabbitMQ; on SIGTERM/SIGINT uvicorn drains HTTP first, then lifespan closes RabbitMQ. `/test-publish` reuses `app.state.rabbitmq`.
- **Files:** `apps/backend/app/cmd/api/main.py`, `apps/backend/tests/cmd/api/test_main_lifespan.py`, `docs/architecture/overview.md`
- **Tests:** `tests/cmd/api/test_main_lifespan.py` — connection closed only after ASGI client (HTTP) context exits
- **Wiki sync:** `docs/architecture/overview.md` — API process lifecycle / shutdown order
- **Open follow-ups:** consumer entrypoint still lacks graceful stop; add when hardening workers
