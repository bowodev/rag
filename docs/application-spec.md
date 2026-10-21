# Virtuascope VCS — Application Spec

**Status:** Locked (v0.5)  
**Language:** English  
**Last updated:** 2026-10-21

---

## 1. Product summary

**VCS** is a **multi-tenant RAG chatbot** platform for the Virtuascope ecosystem.

| Surface | Audience | Responsibility |
|---------|----------|----------------|
| **Dashboard** | Virtuascope users | Manage knowledge (upload/delete), inspect bots, playground chat |
| **Backend** | Platform | API, indexing consumers, retrieval, LLM, tenant isolation |
| **Chatbot / host connect** | Later (P2) | Embed / Photobox-style host integration |

**Bot prompt, model, and LLM parameters are never exposed** via dashboard UI or HTTP APIs. They stay backend-private (loaded in-process for RAG only).

---

## 2. Priority

| Priority | Focus |
|----------|--------|
| **P0 — MVP** | Multi-tenant + RAG pipeline + dashboard knowledge + playground chat |
| **P1** | Hardening (retry, reprocess, observability, rate limits) |
| **P2 — later** | Connect/onboarding to other Virtuascope apps (e.g. Photobox), production embed |

MVP does **not** depend on Photobox/host integration.

---

## 3. Goals & non-goals

### Goals (P0)

- Multi-tenant isolation by `tenant_id`
- Many bots per tenant
- Knowledge: **upload + delete**, clear indexing status
- Playground chat via RAG (retrieve → answer with context)
- Bot settings (prompt/model) stored **backend-private** — never API- or UI-exposed
- Dashboard for Virtuascope users to manage knowledge and test bots

### Non-goals (P0)

- UI to edit prompt / model / temperature
- HTTP APIs that create bots or read/write LLM settings (deferred; settings remain backend-private)
- Connect/onboarding to Photobox or other host apps
- Production embed widget on external sites
- Sharing one knowledge base across many bots
- External connectors (Drive/Notion) or complex crawling
- Analytics / billing
- Fine-tuning / self-hosted LLM serving

---

## 4. Actors (MVP)

| Actor | Role |
|-------|------|
| **VCS User** | Dashboard login; upload/delete knowledge; playground chat |
| **Platform Operator** | Provision users/tenants via internal CRUD; bots + LLM settings configured backend-side (not via exposed ops HTTP in current P0) |
| **System** | Extract/chunk/embed/index; enforce tenant isolation |

Host-app end users are **out of MVP** (relevant in P2).

---

## 5. Domains

```
Tenant ─┬─ User (membership)
        └─ Bot ─┬─ Knowledge
                └─ Chat
```

### 5.1 Tenant

Organization boundary. All resources require `tenant_id`.

### 5.2 User

Dashboard identity. Linked to tenants via **Membership** + role (`owner` / `admin` / `member`).

Platform role: `user` (default) or `ops`. Only `ops` may call `/internal/*` after normal login.

`password_hash` may be null at create time; the user sets a password via `POST /auth/set-password` before they can log in.

### 5.3 Bot

Deployable chatbot unit. Settings (prompt, model, temperature) are **backend-private** — never returned or accepted on HTTP APIs. Dashboard may list bots and status only; it must not edit or display LLM settings.

### 5.4 Knowledge

Per-bot knowledge scope (implicit KB in MVP).

- **Source**: uploaded file — upload & delete
- Status: `processing` | `ready` | `failed`
- **Chunk**: internal indexed pieces + vector pointers
- Indexing pipeline is a **system process**, not a product domain
- Delete source cascades chunks + vectors
- Only `ready` sources participate in retrieval

### 5.5 Chat

- **Conversation** + **Message**
- MVP channel: `playground` only
- Optional citations on assistant messages
- Tied to the dashboard user testing the bot

---

## 6. App responsibilities (MVP)

### Dashboard (`apps/dashboard`)

1. Auth + tenant context  
2. List provisioned bots  
3. Knowledge per bot: upload, delete, show status  
4. Playground chat  
5. **No** prompt/model forms  

### Backend (`apps/backend`)

- Dashboard auth  
- Tenant-scoped reads/writes  
- Source upload/delete + enqueue indexing  
- Consumers: extract → chunk → embed → upsert vectors  
- Playground chat API (retrieve + LLM using **backend-private** settings)  
- Internal APIs for **User + Tenant CRUD** (and memberships)  
- Enforce `tenant_id` (+ `bot_id`) in DB and vector queries  
- **Do not** expose bot create / LLM settings over HTTP in current P0  

### Chatbot (`apps/chatbot`)

Out of P0 critical path. Keep scaffold-friendly; full embed/host UX is P2.

---

## 7. Core flows (MVP)

### Provision

Operator (`ops`) creates tenant + user (+ membership) via internal CRUD (password optional) → user calls `POST /auth/set-password` if hash was null → bots exist via seed/backend-only provisioning with private LLM settings → user sees bot metadata in dashboard.

### Knowledge

User uploads file → Source `processing` → consumer → `ready` | `failed`.  
User deletes source → remove file + chunks + vectors.

### Playground chat

User sends message → persist → retrieve chunks (`tenant_id` + `bot_id`, ready only) → compose prompt (internal system + context + history) → LLM → persist answer (+ citations) → return/stream to UI.

---

## 8. Invariants

1. Every data access is scoped by `tenant_id`
2. Knowledge and Chat are owned by `bot_id` (bot owned by tenant)
3. Prompt/model are backend-private; never exposed via HTTP APIs or dashboard
4. Vector retrieve always filters `tenant_id` + `bot_id`
5. Non-`ready` sources never enter retrieval
6. Deleting a source cleans related index data
7. Users only access tenants where they have membership

---

## 9. API surface (logical, MVP)

```
Auth
  POST /auth/login
  POST /auth/refresh        # exchange refresh JWT for new access (+ refresh) tokens
  POST /auth/set-password   # { email, password } — only when password_hash is null
  GET  /me

Tenants
  GET  /tenants           # membership-scoped; active tenants only

Bots
  GET  /bots
  GET  /bots/{id}          # metadata only — no LLM settings fields

Knowledge
  GET    /bots/{id}/sources
  POST   /bots/{id}/sources
  DELETE /bots/{id}/sources/{sourceId}
  POST   /bots/{id}/sources/{sourceId}/reprocess   # nice-to-have

Chat
  POST /bots/{id}/chat
  GET  /bots/{id}/conversations              # optional
  GET  /conversations/{id}/messages          # optional

Internal (User + Tenant only; require platform_role=ops JWT)
  CRUD + list/filter /internal/tenants
  CRUD + list/filter /internal/users      # password optional on create; never return password_hash
  CRUD + list/filter /internal/memberships

# Explicitly NOT in current P0 API surface:
#   POST  /internal/bots
#   PATCH /internal/bots/{id}/settings
#   authenticated change-password when hash already set
```

---

## 10. Acceptance criteria (P0)

- [ ] Operator (`platform_role=ops`) can CRUD + list/filter users, tenants, and memberships via `/internal/*`
- [ ] Non-ops callers cannot use `/internal/*`
- [ ] User with null password_hash can set password via `/auth/set-password` then login
- [ ] Dashboard user only sees bots in their tenant(s)
- [ ] Upload file → status becomes `ready` (or visible `failed`)
- [ ] Delete file → content no longer used in answers
- [ ] Playground answers using relevant knowledge context
- [ ] Tenant/bot A cannot retrieve Tenant/bot B knowledge
- [ ] Dashboard does not expose prompt/model editing
- [ ] No HTTP API returns or accepts bot LLM settings
- [ ] Empty knowledge: bot can still answer from default prompt without inventing KB facts

---

## 11. Later (P2) — connect & host apps

Low priority. Direction only:

- Connection: host app (e.g. Photobox) ↔ VCS bot
- Onboard API + credentials
- Host chat channel
- Embed/widget if needed

Anticipated rules (do not implement in P0 unless explicitly requested):

- Binding `(host_app, external_id)` → one bot
- Idempotent onboard; reconnect reuses bot so knowledge is preserved
- Host auth uses connection token, not dashboard JWT

---

## 12. Open decisions

1. MVP file types: PDF + TXT, or also DOCX?
2. ~~Vector store: pgvector (proposed) vs Qdrant~~ **Resolved:** pgvector (same Postgres instance; `chunk_embeddings` + `tenant_id`/`bot_id` filters)
3. ~~Dashboard auth: managed vs self-hosted JWT~~ **Resolved (VCS-002):** self-hosted HS256 JWT (access + refresh); managed IdP deferred
4. ~~Bot creation: internal-only vs “request bot”?~~ **Resolved (v0.4):** no HTTP bot/LLM-settings APIs in current P0; bots via seed/backend-only; internal APIs = User + Tenant CRUD; LLM settings never exposed
5. Failed-source reprocess: P0 or P1?
6. ~~Internal ops auth~~ **Resolved (VCS-003):** same login JWT; `users.platform_role = ops` + `require_ops`
7. ~~Password provisioning~~ **Resolved (VCS-003):** ops may create users with null hash; self-serve `POST /auth/set-password` (first-time only)
