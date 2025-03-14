"""init_table_questionnaire

Revision ID: cd1bc3eb2cfb
Revises: 978093f94bbb
Create Date: 2025-03-14 09:56:53.680120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'cd1bc3eb2cfb'
down_revision: Union[str, None] = '978093f94bbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('questionnaire',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для сохранения структуры анкеты'
    )
    op.add_column('survey', sa.Column('questionnaire_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'survey', 'questionnaire', ['questionnaire_id'], ['id'])


def downgrade() -> None:
    op.drop_column('survey', 'questionnaire_id')
    op.drop_table('questionnaire')

