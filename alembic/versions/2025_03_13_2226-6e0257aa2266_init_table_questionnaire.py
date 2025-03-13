"""init_table_questionnaire

Revision ID: 6e0257aa2266
Revises: 978093f94bbb
Create Date: 2025-03-13 22:26:09.428013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6e0257aa2266'
down_revision: Union[str, None] = '978093f94bbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('questionnaire',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False, comment='Идентификатор записи'),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для сохранения структуры анкеты'
    )
    op.add_column('survey', sa.Column('questionnaire', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'survey', 'questionnaire', ['questionnaire'], ['id'])



def downgrade() -> None:
    op.drop_constraint(None, 'survey', type_='foreignkey')
    op.drop_column('survey', 'questionnaire')
    op.drop_table('questionnaire')

