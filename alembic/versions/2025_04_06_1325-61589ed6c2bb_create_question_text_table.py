"""create question text table

Revision ID: 61589ed6c2bb
Revises: 44cc2e741554
Create Date: 2025-04-06 13:25:02.243625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '61589ed6c2bb'
down_revision: Union[str, None] = '44cc2e741554'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('question_text',
    sa.Column('questionnaire_question_id', sa.Uuid(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.ForeignKeyConstraint(['questionnaire_question_id'], ['questionnaire_question.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для хранения текста вопроса анкеты'
    )
    op.drop_column('questionnaire_question', 'written_text')
    op.drop_column('questionnaire_question', 'choice_text')


def downgrade() -> None:
    op.add_column('questionnaire_question', sa.Column('choice_text', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True, comment='Список вопросов для множественного выбора. Зависит от типа'))
    op.add_column('questionnaire_question', sa.Column('written_text', sa.VARCHAR(), autoincrement=False, nullable=True, comment='Текст вопроса для письменного ответа. Зависит от типа'))
    op.drop_table('question_text')
