from enum import StrEnum

from sqlalchemy import Enum as SAEnum


def pg_str_enum(enum_cls: type[StrEnum], *, name: str) -> SAEnum:
    """Postgres ENUM that stores StrEnum *values* (e.g. 'active'), not member names."""
    return SAEnum(
        enum_cls,
        name=name,
        values_callable=lambda members: [m.value for m in members],
        native_enum=True,
        validate_strings=True,
    )
