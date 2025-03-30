"""rebuild-relation-survey-to-questionnaire

Revision ID: 173a83e35143
Revises: 6ffd70da6a05
Create Date: 2025-03-30 13:26:08.884639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '173a83e35143'
down_revision: Union[str, None] = '6ffd70da6a05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('questionnaire', sa.Column('survey_id', sa.UUID(), nullable=True))
    op.execute("""
        UPDATE questionnaire q
        SET survey_id = s.id
        FROM survey s
        WHERE s.questionnaire_id = q.id
    """)
    op.drop_constraint('survey_questionnaire_id_fkey', 'survey', type_='foreignkey')
    op.drop_column('survey', 'questionnaire_id')


def downgrade():
    op.add_column('survey', sa.Column('questionnaire_id', sa.UUID(), nullable=True))
    op.execute("""
        UPDATE survey s
        SET questionnaire_id = q.id
        FROM questionnaire q
        WHERE q.survey_id = s.id
    """)
    op.create_foreign_key('survey_questionnaire_id_fkey', 'survey', 'questionnaire', ['questionnaire_id'], ['id'])
    op.drop_column('questionnaire', 'survey_id')
