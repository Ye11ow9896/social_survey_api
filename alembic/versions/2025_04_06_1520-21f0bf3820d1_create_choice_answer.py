"""create choice answer

Revision ID: 21f0bf3820d1
Revises: 61589ed6c2bb
Create Date: 2025-04-06 15:20:18.329507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21f0bf3820d1'
down_revision: Union[str, None] = '61589ed6c2bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('choice_answer',
    sa.Column('question_text_id', sa.Uuid(), nullable=False),
    sa.Column('question_id', sa.Uuid(), nullable=False),
    sa.Column('telegram_user_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.ForeignKeyConstraint(['question_id'], ['questionnaire_question.id'], ),
    sa.ForeignKeyConstraint(['question_text_id'], ['question_text.id'], ),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['telegram_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('question_id', 'telegram_user_id', name='uq_question_id_telegram_user_id_question_text_id'),
    comment='Таблица для хранения ответа с выбором(множественным и единственным из нескольких)'
    )


def downgrade() -> None:
    op.drop_table('choice_answer')
