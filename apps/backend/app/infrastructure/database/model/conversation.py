import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.infrastructure.database.enum import ConversationChannel
from app.infrastructure.database.types import pg_str_enum


class Conversation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "conversations"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "bot_id"],
            ["bots.tenant_id", "bots.id"],
            name="fk_conversations_tenant_bot",
        ),
        Index("ix_conversations_tenant_bot", "tenant_id", "bot_id"),
        Index("ix_conversations_bot_user", "bot_id", "user_id"),
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )
    bot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    channel: Mapped[ConversationChannel] = mapped_column(
        pg_str_enum(ConversationChannel, name="conversation_channel"),
        default=ConversationChannel.PLAYGROUND,
        server_default=ConversationChannel.PLAYGROUND.value,
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(String, nullable=True)
