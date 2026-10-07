# Domain: User

## Purpose

Identify dashboard users and their access to tenants.

## Core concepts

- **User**: id, email, name
- **Membership**: user ↔ tenant + role (`owner` / `admin` / `member`)

## Invariants

- A user may belong to multiple tenants
- Dashboard access requires an active membership for the selected tenant

## Out of scope

- Host-app end users / anonymous visitors (P2)

## Collaborates with

- **Tenant**
- Initiates **Chat** in playground
