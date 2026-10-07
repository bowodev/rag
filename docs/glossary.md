# Glossary

| Term | Meaning |
|------|---------|
| **Tenant** | Organization boundary; all data is isolated by `tenant_id` |
| **User** | Person who signs into the VCS dashboard |
| **Membership** | Link between User and Tenant with a role |
| **Bot** | Chatbot configuration unit owned by a tenant |
| **Knowledge** | Per-bot knowledge scope used for retrieval |
| **Source** | Original knowledge input (file in MVP) |
| **Chunk** | Indexed fragment of a Source (internal technical concept) |
| **Chat** | Conversations and messages with a Bot |
| **Playground** | Dashboard chat channel for testing RAG |
| **Operator** | Internal role that provisions bots and sets prompt/model |
| **Connection** | P2 concept: host app binding to a Bot (not MVP) |

Do **not** treat indexing jobs, extractors, or embedders as product domains. They are system processes inside Knowledge.
