"""rebild_rolecodeenum_add_owner

Revision ID: caeeabde5f20
Revises: cd1bc3eb2cfb
Create Date: 2025-03-17 20:39:43.211959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caeeabde5f20'
down_revision: Union[str, None] = 'cd1bc3eb2cfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.execute("ALTER TYPE rolecodeenum RENAME TO rolecodeenum_old;")
    op.execute("CREATE TYPE rolecodeenum AS ENUM ('ADMIN', 'RESPONDENT', 'OWNER');")
    op.execute('ALTER TABLE role ALTER COLUMN code TYPE rolecodeenum USING code::text::rolecodeenum;')
    op.execute("DROP TYPE rolecodeenum_old;")

def downgrade():
    op.execute("ALTER TYPE rolecodeenum RENAME TO rolecodeenum_old;")
    op.execute("CREATE TYPE rolecodeenum AS ENUM ('ADMIN', 'RESPONDENT');")
    op.execute('ALTER TABLE role ALTER COLUMN code TYPE rolecodeenum USING code::text::rolecodeenum;')
    op.execute("DROP TYPE rolecodeenum_old;")