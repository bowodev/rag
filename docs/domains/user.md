# Domain: User

## Purpose

Identify dashboard users and their access to tenants.

## Core concepts

- **User**: id, email, name, password_hash (nullable until set)
- **Membership**: user ↔ tenant + role (`owner` / `admin` / `member`)
- **Dashboard auth**: self-hosted JWT — short-lived access + longer-lived refresh (`POST /auth/login`, `POST /auth/refresh`)

## Invariants

- A user may belong to multiple tenants
- Dashboard access requires an active membership for the selected tenant
- Access tokens authenticate identity only; tenant authorization uses membership checks

## Out of scope

- Host-app end users / anonymous visitors (P2)

## Collaborates with

- **Tenant**
- Initiates **Chat** in playground
