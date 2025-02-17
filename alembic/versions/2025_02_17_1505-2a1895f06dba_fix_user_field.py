"""fix user field

Revision ID: 2a1895f06dba
Revises: 6e2a00717562
Create Date: 2025-02-17 15:05:21.505520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a1895f06dba'
down_revision: Union[str, None] = '6e2a00717562'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('telegram_user', sa.Column('url', sa.String(), nullable=False, comment='Cсылка типа tg://user?id=54763794. Одноименно переменной в aiogram'))
    op.drop_column('telegram_user', 'Cсылка типа tg://user?id=54763794. Одноименн')



def downgrade() -> None:
    op.add_column('telegram_user', sa.Column('Cсылка типа tg://user?id=54763794. Одноименн', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('telegram_user', 'url')

