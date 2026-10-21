from enum import StrEnum

class SourceStatus(StrEnum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

class TenantStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"

class MembershipRole(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"
    OWNER = "owner"


class PlatformRole(StrEnum):
    USER = "user"
    OPS = "ops"

class BotStatus(StrEnum):
    DRAFT = "draft"
    LIVE = "live"
    DISABLED = "disabled"

class ConversationChannel(StrEnum):
    PLAYGROUND = "playground"

class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"