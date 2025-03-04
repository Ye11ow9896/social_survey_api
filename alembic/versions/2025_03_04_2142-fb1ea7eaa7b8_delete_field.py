"""delete field

Revision ID: fb1ea7eaa7b8
Revises: 2292a61b2fea
Create Date: 2025-03-04 21:42:54.035986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb1ea7eaa7b8'
down_revision: Union[str, None] = '2292a61b2fea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('survey_telegram_respondent_id_fkey', 'survey', type_='foreignkey')
    op.drop_column('survey', 'telegram_respondent_id')


def downgrade() -> None:
    op.add_column('survey', sa.Column('telegram_respondent_id', sa.UUID(), autoincrement=False, nullable=False, comment='Ключ таблицы респондентов с тг. Аналогичное добавление планируется для других источников трафика'))
    op.create_foreign_key('survey_telegram_respondent_id_fkey', 'survey', 'telegram_user', ['telegram_respondent_id'], ['id'])
