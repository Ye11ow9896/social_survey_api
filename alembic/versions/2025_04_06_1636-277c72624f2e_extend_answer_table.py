"""extend answer table

Revision ID: 277c72624f2e
Revises: d15c65567069
Create Date: 2025-04-06 16:36:06.301031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '277c72624f2e'
down_revision: Union[str, None] = 'd15c65567069'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('question_answer', sa.Column('text', sa.String(), nullable=True, comment='Заполняется только для текстового ответа'))


def downgrade() -> None:
    op.drop_column('question_answer', 'text')
