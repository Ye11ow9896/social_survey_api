"""add questionnaire question table

Revision ID: 7fa774255299
Revises: cd1bc3eb2cfb
Create Date: 2025-03-19 21:13:35.096734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7fa774255299'
down_revision: Union[str, None] = 'cd1bc3eb2cfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('questionnaire_question',
    sa.Column('question_text', sa.String(), nullable=False, comment='Текст вопроса анкеты'),
    sa.Column('number', sa.Integer(), nullable=False, comment='Порядковый номер вопроса анкеты'),
    sa.Column('choice_text', sa.ARRAY(sa.String()), nullable=True, comment='Список вопросов для множественного выбора. Зависит от типа'),
    sa.Column('question_type', sa.Enum('WRITTEN', 'MULTIPLE_CHOICE', 'ONE_CHOICE', name='questiontype'), nullable=False, comment='Тип вопроса'),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для хранения вопросов для анкеты'
    )
    op.add_column('questionnaire', sa.Column('question_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'questionnaire', 'questionnaire_question', ['question_id'], ['id'])
    op.create_table_comment(
        'questionnaire',
        'Таблица для хранения анкеты',
        existing_comment='Таблица для сохранения структуры анкеты',
        schema=None
    )
    op.drop_column('questionnaire', 'data')


def downgrade() -> None:
    op.add_column('questionnaire', sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.create_table_comment(
        'questionnaire',
        'Таблица для сохранения структуры анкеты',
        existing_comment='Таблица для хранения анкеты',
        schema=None
    )
    op.drop_column('questionnaire', 'question_id')
    op.drop_table('questionnaire_question')
    op.execute('DROP TYPE IF EXISTS questiontype')
