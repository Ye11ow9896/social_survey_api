"""init_table_user_admin

Revision ID: 978093f94bbb
Revises: fb1ea7eaa7b8
Create Date: 2025-03-12 17:32:07.088932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '978093f94bbb'
down_revision: Union[str, None] = 'fb1ea7eaa7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user_admin',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(length=32), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для авторицации с паролем и пользователем'
    )


def downgrade() -> None:
    op.drop_table('user_admin')

