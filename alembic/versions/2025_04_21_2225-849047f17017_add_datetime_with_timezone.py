"""add datetime with timezone

Revision ID: 849047f17017
Revises: 359ca06b0511
Create Date: 2025-04-21 22:25:47.841903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '849047f17017'
down_revision: Union[str, None] = '359ca06b0511'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('telegram_owner__survey', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_comment='Дата назначения респондента на исследование',
               existing_nullable=False)
    op.alter_column('telegram_respondent__questionnaire', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_comment='Дата назначения анкеты на респондента',
               existing_nullable=False)


def downgrade() -> None:
    op.alter_column('telegram_respondent__questionnaire', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_comment='Дата назначения анкеты на респондента',
               existing_nullable=False)
    op.alter_column('telegram_owner__survey', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_comment='Дата назначения респондента на исследование',
               existing_nullable=False)
