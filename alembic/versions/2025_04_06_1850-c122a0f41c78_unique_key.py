"""unique key

Revision ID: c122a0f41c78
Revises: 277c72624f2e
Create Date: 2025-04-06 18:50:16.916014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c122a0f41c78'
down_revision: Union[str, None] = '277c72624f2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('uq_question_id_user_id_question_text_id', 'question_answer', type_='unique')
    op.create_unique_constraint('uq_question_id_user_id_question_text_id', 'question_answer', ['question_id', 'telegram_user_id', 'question_text_id'])


def downgrade() -> None:
    op.drop_constraint('uq_question_id_user_id_question_text_id', 'question_answer', type_='unique')
    op.create_unique_constraint('uq_question_id_user_id_question_text_id', 'question_answer', ['question_id', 'telegram_user_id'])
