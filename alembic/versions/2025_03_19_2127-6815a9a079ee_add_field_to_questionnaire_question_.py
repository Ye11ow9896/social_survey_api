"""add field to questionnaire question table

Revision ID: 6815a9a079ee
Revises: 7fa774255299
Create Date: 2025-03-19 21:27:26.868554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6815a9a079ee'
down_revision: Union[str, None] = '7fa774255299'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('questionnaire_question', sa.Column('written_text', sa.String(), nullable=True, comment='Текст вопроса для письменного ответа. Зависит от типа'))


def downgrade() -> None:
    op.drop_column('questionnaire_question', 'written_text')
