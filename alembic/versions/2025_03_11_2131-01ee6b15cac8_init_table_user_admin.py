"""init_table_user_admin

Revision ID: 01ee6b15cac8
Revises: fb1ea7eaa7b8
Create Date: 2025-03-11 21:31:21.549881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01ee6b15cac8'
down_revision: Union[str, None] = 'fb1ea7eaa7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_admin',
    sa.Column('username', sa.Uuid(), nullable=False),
    sa.Column('hashed_password', sa.String(length=16), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для авторицации с паролем и пользователем'
    )


def downgrade() -> None:
    op.drop_table('user_admin')


