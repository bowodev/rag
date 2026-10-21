from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.infrastructure.database.enum import PlatformRole
from app.infrastructure.database.types import pg_str_enum


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    platform_role: Mapped[PlatformRole] = mapped_column(
        pg_str_enum(PlatformRole, name="platform_role"),
        default=PlatformRole.USER,
        server_default=PlatformRole.USER.value,
        nullable=False,
    )