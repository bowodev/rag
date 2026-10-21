import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.infrastructure.database.enum import BotStatus
from app.infrastructure.database.types import pg_str_enum


class Bot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "bots"
    __table_args__ = (
        UniqueConstraint("tenant_id", "id", name="uq_bots_tenant_id"),
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[BotStatus] = mapped_column(
        pg_str_enum(BotStatus, name="bot_status"),
        default=BotStatus.DRAFT,
        server_default=BotStatus.DRAFT.value,
        nullable=False,
    )
