# Domain: User

## Purpose

Identify dashboard users and their access to tenants; distinguish platform operators.

## Core concepts

- **User**: id, email, name, password_hash (nullable until set), `platform_role` (`user` \| `ops`, default `user`)
- **Membership**: user ↔ tenant + role (`owner` / `admin` / `member`)
- **Dashboard auth**: self-hosted JWT — short-lived access + longer-lived refresh (`POST /auth/login`, `POST /auth/refresh`)
- **Set password**: `POST /auth/set-password` — first-time only when `password_hash` is null
- **Ops**: users with `platform_role = ops` may call `/internal/*` after normal login

## Invariants

- A user may belong to multiple tenants
- Dashboard access requires an active membership for the selected tenant
- Access tokens authenticate identity (+ platform role for ops gates); tenant authorization uses membership checks
- Login requires a non-null `password_hash` and a matching password
- Ops may create users without a password; the user must set it themselves before login
- Once `password_hash` is set, first-time set-password must not overwrite it (no change-password in current P0 surface)
- HTTP responses never expose `password_hash`
- Hard delete of a user removes their memberships first

## Out of scope

- Host-app end users / anonymous visitors (P2)
- Authenticated change-password / reset-via-email flows

## Collaborates with

- **Tenant**
- Initiates **Chat** in playground
