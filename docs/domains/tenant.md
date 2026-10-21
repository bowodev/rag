# Domain: Tenant

## Purpose

Define the organization boundary and multi-tenant isolation root.

## Core concepts

- **Tenant**: id, name, slug, status (`active` / `suspended`)
- **Internal ops**: full CRUD + list/filter under `/internal/tenants` (ops JWT only)

## Invariants

- Every business resource references a `tenant_id`
- Cross-tenant reads/writes are forbidden
- `GET /tenants` returns only tenants where the caller has membership (active tenants)
- Path/body `tenant_id` must pass `require_tenant_membership` before use
- Hard delete of a tenant removes memberships first; fails with conflict if bots/other owned resources still exist

## Out of scope

- Bot prompts, knowledge files, chat messages

## Collaborates with

- **User** via Membership
- Owns **Bot**
