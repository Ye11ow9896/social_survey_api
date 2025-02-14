"""crate user table

Revision ID: 0118288f5b1a
Revises:
Create Date: 2025-01-19 20:31:48.357232

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0118288f5b1a"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("second_name", sa.String(), nullable=True),
        sa.Column("hash_password", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("user")
