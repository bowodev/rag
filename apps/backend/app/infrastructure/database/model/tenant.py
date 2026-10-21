from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.infrastructure.database.enum import TenantStatus
from app.infrastructure.database.types import pg_str_enum


class Tenant(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[TenantStatus] = mapped_column(
        pg_str_enum(TenantStatus, name="tenant_status"),
        default=TenantStatus.ACTIVE,
        server_default=TenantStatus.ACTIVE.value,
        nullable=False,
    )
