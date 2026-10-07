# Domain: Bot

## Purpose

Represent a provisioned chatbot that owns knowledge and chat.

## Core concepts

- **Bot** (Postgres metadata): id, tenant_id, name, status (`draft` / `live` / `disabled`)
- **Settings (backend-private, config — not DB in MVP)**: system prompt, model, temperature, related LLM params — never exposed via HTTP or dashboard; per-tenant prompt editing is out of scope for MVP
- Dashboard may **read** bot metadata; it must **not** edit or display LLM settings in MVP

## Invariants

- Bot always belongs to exactly one tenant
- Prompt/model/temperature come from backend config (in-process for RAG only); not columns on `bots`; no HTTP read/write of LLM settings in current P0

## Out of scope

- Source files and chunks (Knowledge)
- Message history (Chat)
- Host connection binding (P2)

## Collaborates with

- Owns **Knowledge** and **Chat**
