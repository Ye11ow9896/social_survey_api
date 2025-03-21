"""tg_id type bigint

Revision ID: 6ffd70da6a05
Revises: 48e1e9581788
Create Date: 2025-03-22 00:25:47.590236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ffd70da6a05'
down_revision: Union[str, None] = '48e1e9581788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('telegram_user', 'tg_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_comment='Идентификатор в тг. в aiogram - id',
               existing_nullable=False)


def downgrade() -> None:
    op.alter_column('telegram_user', 'tg_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_comment='Идентификатор в тг. в aiogram - id',
               existing_nullable=False)
