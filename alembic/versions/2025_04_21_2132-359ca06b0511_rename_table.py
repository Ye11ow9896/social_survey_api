"""rename table

Revision ID: 359ca06b0511
Revises: d64bb6a6edb4
Create Date: 2025-04-21 21:32:45.934101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '359ca06b0511'
down_revision: Union[str, None] = 'd64bb6a6edb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('telegram_owner__survey',
    sa.Column('telegram_user_id', sa.Uuid(), nullable=False, comment='Ключ таблицы telegram_user'),
    sa.Column('survey_id', sa.Uuid(), nullable=False, comment='Ключ таблицы исследования'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='Дата назначения респондента на исследование'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['telegram_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('telegram_user_id', 'survey_id', 'id'),
    comment='Таблица для хранения респондентов'
    )
    op.drop_table('telegram_respondent__survey')


def downgrade() -> None:
    op.create_table('telegram_respondent__survey',
    sa.Column('telegram_user_id', sa.UUID(), autoincrement=False, nullable=False, comment='Ключ таблицы telegram_user'),
    sa.Column('survey_id', sa.UUID(), autoincrement=False, nullable=False, comment='Ключ таблицы исследования'),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False, comment='Дата назначения респондента на исследование'),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False, comment='Идентификатор записи'),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], name='telegram_respondent__survey_survey_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['telegram_user.id'], name='telegram_respondent__survey_telegram_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('telegram_user_id', 'survey_id', 'id', name='telegram_respondent__survey_pkey'),
    comment='Таблица для хранения респондентов'
    )
    op.drop_table('telegram_owner__survey')
