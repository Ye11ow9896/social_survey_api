"""fix type fields

Revision ID: 2292a61b2fea
Revises: 01828b950fb0
Create Date: 2025-02-19 21:52:23.694797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2292a61b2fea'
down_revision: Union[str, None] = '01828b950fb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'telegram_user', ['tg_id'])


def downgrade() -> None:
    op.drop_constraint(None, 'telegram_user', type_='unique')

