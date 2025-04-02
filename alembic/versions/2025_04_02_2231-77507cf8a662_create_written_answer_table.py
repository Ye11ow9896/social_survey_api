"""create written answer table

Revision ID: 77507cf8a662
Revises: 0f52d3ac940e
Create Date: 2025-04-02 22:31:27.100333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77507cf8a662'
down_revision: Union[str, None] = '0f52d3ac940e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('written_answer',
    sa.Column('text', sa.String(), nullable=False, comment='Текст ответа на вопрос'),
    sa.Column('question_id', sa.Uuid(), nullable=False),
    sa.Column('telegram_user_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.ForeignKeyConstraint(['question_id'], ['questionnaire.id'], ),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['questionnaire.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для хранения ответа на письменный вопрос'
    )


def downgrade() -> None:
    op.drop_table('written_answer')
