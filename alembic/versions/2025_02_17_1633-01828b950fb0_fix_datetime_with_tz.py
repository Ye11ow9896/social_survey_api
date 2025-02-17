"""fix datetime with tz

Revision ID: 01828b950fb0
Revises: 2a1895f06dba
Create Date: 2025-02-17 16:33:18.752891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '01828b950fb0'
down_revision: Union[str, None] = '2a1895f06dba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('auth_service', 'id',
               existing_type=sa.UUID(),
               comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('role', 'id',
               existing_type=sa.UUID(),
               comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('survey', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.alter_column('survey', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.alter_column('survey', 'id',
               existing_type=sa.UUID(),
               comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('telegram_respondent__survey', 'id',
               existing_type=sa.UUID(),
               comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('telegram_user', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False)
    op.alter_column('telegram_user', 'id',
               existing_type=sa.UUID(),
               comment='Идентификатор записи',
               existing_nullable=False)


def downgrade() -> None:
    op.alter_column('telegram_user', 'id',
               existing_type=sa.UUID(),
               comment=None,
               existing_comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('telegram_user', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('telegram_respondent__survey', 'id',
               existing_type=sa.UUID(),
               comment=None,
               existing_comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('survey', 'id',
               existing_type=sa.UUID(),
               comment=None,
               existing_comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('survey', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('survey', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('role', 'id',
               existing_type=sa.UUID(),
               comment=None,
               existing_comment='Идентификатор записи',
               existing_nullable=False)
    op.alter_column('auth_service', 'id',
               existing_type=sa.UUID(),
               comment=None,
               existing_comment='Идентификатор записи',
               existing_nullable=False)
