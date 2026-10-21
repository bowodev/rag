# Backend architecture

**Path:** `apps/backend`  
**Last updated:** 2026-10-21

Clean architecture under `apps/backend/app/`. HTTP and queue entrypoints stay thin; business rules live in application/domain.

## Layer map

```text
cmd/            process entrypoints (API + consumers)
  api/          FastAPI app, routes, deps, error mapping
  consumer/     registry + runner for RabbitMQ workers
presenter/      HTTP / event adapters (map errors → API responses)
middleware/     cross-cutting helpers used by deps (e.g. AuthMiddleware)
application/    use-cases + ports (interfaces) + bootstrap services
domain/         DTOs, auth context, domain errors (no I/O)
infrastructure/ adapters: DB, JWT, RabbitMQ, vector readiness
config/         settings (env)
```

Dependency direction: **cmd → presenter → application → domain**; **infrastructure** implements **application/ports**.

## Request path (HTTP)

```text
Route (cmd/api/routes)
  → Presenter (presenter/*_http_handler)
    → Application service / use-case (application/*)
      → Port (application/ports)
        → Infrastructure repo / JWT / bus
```

Example (auth):

1. `POST /auth/login` in `cmd/api/routes/auth.py`
2. `AuthHTTPHandler.login` maps `ValidationError` / `UnauthorizedError` → HTTP errors
3. `AuthService` (`application/auth/bootstrap.py`) runs `Login` / `Refresh`
4. `UserRepository` + `infrastructure/auth/jwt.py` persist/read and mint tokens

Protected routes use FastAPI deps in `cmd/api/deps/auth.py`:

- `require_auth` — Bearer access JWT → `AuthContext`
- `require_tenant_membership` — membership check for a given `tenant_id`

## Consumer path (queue)

```text
cmd/consumer/main
  → registry ConsumerSpec (queue + Pydantic model + presenter)
    → runner consumes RabbitMQ
      → presenter handler (application / infrastructure work)
```

Today a **test** consumer is registered (`IndexSource` job shape). Knowledge indexing consumers plug into the same registry pattern.

## Persistence

| Piece | Location |
|-------|----------|
| SQLAlchemy models | `infrastructure/database/model/` |
| Repositories | `infrastructure/database/repository/` |
| Session / engine | `infrastructure/database/session.py` |
| Migrations | `alembic/` |
| Logical schema | [`schema.dbml`](./schema.dbml) |

## Messaging

| Piece | Location |
|-------|----------|
| Connection (API lifespan) | `infrastructure/rabbitmq/connection.py` |
| Publish bus | `infrastructure/rabbitmq/bus.py` (`RabbitMQBus`) |
| Job DTOs | `domain/dto/jobs.py` |
| Port | `application/ports/job_bus.py` |

## Auth primitives

| Piece | Location |
|-------|----------|
| JWT encode/decode | `infrastructure/auth/jwt.py` |
| Login / refresh use-cases | `application/auth/` |
| Password hashing | `application/auth/password_helper.py` |
| `AuthContext` / login DTOs | `domain/auth/` |
| Token → user | `middleware/auth.py` + `cmd/api/deps/auth.py` |

## Conventions

- Routers stay thin; no business rules in routes
- Repositories always accept `tenant_id` (and `bot_id` when bot-owned) — see [`multi-tenancy.md`](./multi-tenancy.md)
- Ports in `application/ports/`; wire concrete adapters in bootstrap / deps
- Prefer explicit types; fail closed on authz
- Unit tests mirror layers under `apps/backend/tests/`
