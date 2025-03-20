"""empty message

Revision ID: 48e1e9581788
Revises: caeeabde5f20, fda02ebedb9b
Create Date: 2025-03-20 23:44:56.301394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48e1e9581788'
down_revision: Union[str, None] = ('caeeabde5f20', 'fda02ebedb9b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
