# Domain: Tenant

## Purpose

Define the organization boundary and multi-tenant isolation root.

## Core concepts

- **Tenant**: id, name, slug, status (`active` / `suspended`)

## Invariants

- Every business resource references a `tenant_id`
- Cross-tenant reads/writes are forbidden
- `GET /tenants` returns only tenants where the caller has membership (active tenants)
- Path/body `tenant_id` must pass `require_tenant_membership` before use

## Out of scope

- Bot prompts, knowledge files, chat messages

## Collaborates with

- **User** via Membership
- Owns **Bot**
