"""add users.platform_role

Revision ID: 002
Revises: 001
Create Date: 2026-10-21

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "002"
down_revision: Union[str, Sequence[str], None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("CREATE TYPE platform_role AS ENUM ('user', 'ops')"))
    platform_role = postgresql.ENUM(
        "user", "ops", name="platform_role", create_type=False
    )
    op.add_column(
        "users",
        sa.Column(
            "platform_role",
            platform_role,
            server_default="user",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "platform_role")
    op.execute(sa.text("DROP TYPE platform_role"))
