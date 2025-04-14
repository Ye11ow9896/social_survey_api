"""add telegram_respondent__questionnaire table

Revision ID: d64bb6a6edb4
Revises: b14ba935976a
Create Date: 2025-04-14 15:01:35.391070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd64bb6a6edb4'
down_revision: Union[str, None] = 'b14ba935976a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('telegram_respondent__questionnaire',
    sa.Column('telegram_user_id', sa.Uuid(), nullable=False, comment='Ключ таблицы telegram_user'),
    sa.Column('questionnaire_id', sa.Uuid(), nullable=False, comment='Ключ таблицы анкет'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='Дата назначения анкеты на респондента'),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.ForeignKeyConstraint(['questionnaire_id'], ['questionnaire.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['telegram_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('telegram_user_id', 'questionnaire_id', 'id'),
    comment='Таблица для хранения назначенных анкет на респондентов'
    )


def downgrade() -> None:
    op.drop_table('telegram_respondent__questionnaire')
