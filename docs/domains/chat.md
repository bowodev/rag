# Domain: Chat

## Purpose

Capture conversations between a dashboard user (playground) and a bot.

## Core concepts

- **Conversation**: session for a bot + channel
- **Message**: role (`user` | `assistant`), content, timestamps
- Optional **citations** linking assistant answers to knowledge sources/chunks

## MVP channel

- `playground` only

## Invariants

- Messages belong to a conversation owned by a bot (`tenant_id` implied via bot)
- Retrieval from Knowledge happens when generating an assistant reply; it is collaboration, not a Chat entity

## Out of scope

- Host-app / plugin channels (P2)
- Prompt/model storage
