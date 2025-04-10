"""update_questionnaire_add_question_text

Revision ID: b14ba935976a
Revises: c122a0f41c78
Create Date: 2025-04-09 20:17:44.976496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b14ba935976a'
down_revision: Union[str, None] = 'c122a0f41c78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('questionnaire_question', sa.Column('question_text', sa.String(), nullable=True))
    op.execute(f"UPDATE questionnaire_question SET question_text = 'default_value'")
    op.alter_column('questionnaire_question', 'question_text', nullable=False)


def downgrade() -> None:
    op.drop_column('questionnaire_question', 'question_text')
