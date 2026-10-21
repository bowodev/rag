# 2026-10-21 — VCS-004 Bots read APIs (metadata only)

## Summary

Implemented `GET /bots` and `GET /bots/{id}` returning safe bot metadata for the caller’s membership tenants.

## Decisions

- List across all membership tenants (no selected-tenant header/query)
- Cross-tenant / missing → 403 `bot access denied`
- All statuses; fields: id, name, status, tenant_id, created_at, updated_at
- No LLM settings fields (none on `bots` table; DTO omits them)

## Verify

- `uv run pytest tests/application/bot/test_list_and_get_for_user.py`
