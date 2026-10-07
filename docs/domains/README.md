# Domains

Canonical domains for VCS (see also [Application Spec](../application-spec.md)):

1. [Tenant](./tenant.md)
2. [User](./user.md)
3. [Bot](./bot.md)
4. [Knowledge](./knowledge.md)
5. [Chat](./chat.md)

## Relationship map

```text
Tenant ─┬─ User (via Membership)
        └─ Bot ─┬─ Knowledge (Sources / Chunks)
                └─ Chat (Conversations / Messages)
```

## Rules

- Prefer nouns and product language in domain docs.
- System verbs (ingest, extract, embed) belong in architecture/backend docs, not as top-level domains.
- Agents must not invent extra domains without an explicit docs/ticket update.
