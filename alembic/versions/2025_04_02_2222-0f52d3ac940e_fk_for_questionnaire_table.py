"""create written answer table

Revision ID: 0f52d3ac940e
Revises: 173a83e35143
Create Date: 2025-04-02 22:22:16.775376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f52d3ac940e'
down_revision: Union[str, None] = '173a83e35143'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(None, 'questionnaire', 'survey', ['survey_id'], ['id'])


def downgrade() -> None:
    pass
