"""init tables

Revision ID: a97dd6eca1df
Revises: 
Create Date: 2025-02-15 20:28:14.285139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97dd6eca1df'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('auth_service',
    sa.Column('service_name', sa.String(), nullable=False, comment='Название сервиса для получения доступа к API'),
    sa.Column('hash_password', sa.String(), nullable=False, comment='Хэш пароля сервиса'),
    sa.Column('hash_password_updated_at', sa.Date(), nullable=False, comment='Дата обновления пароля. На будущее, когда будет функцинал обновления пароля. Например раз в 3 месяца'),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для хранения подключенных сервисов к API'
    )
    op.create_table('role',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.Enum('ADMIN', 'RESPONDENT', name='rolecodeenum'), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для храненияролей пользаков. пока роль будет так храниться, создана для возможного расширения функционала ролей'
    )
    op.create_table('telegram_user',
    sa.Column('tg_id', sa.Integer(), nullable=False, comment='Идентификатор в тг. в aiogram - id'),
    sa.Column('username', sa.String(), nullable=True, comment='Акк в тг. Одноименно переменной в aiogram'),
    sa.Column('first_name', sa.String(), nullable=True, comment='first_name. Одноименно переменной в aiogram'),
    sa.Column('last_name', sa.String(), nullable=True, comment='last_name. Одноименно переменной в aiogram'),
    sa.Column('Cсылка типа tg://user?id=54763794. Одноименно переменной в aiogram', sa.String(), nullable=False),
    sa.Column('is_bot', sa.Boolean(), nullable=False, comment='Одноименно переменной в aiogram'),
    sa.Column('is_premium', sa.Boolean(), nullable=False, comment='Одноименно переменной в aiogram'),
    sa.Column('role_id', sa.Uuid(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('real_first_name', sa.String(), nullable=True),
    sa.Column('real_middle_name', sa.String(), nullable=True),
    sa.Column('real_last_name', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для хранения пользаков из телеграма'
    )
    op.create_table('survey',
    sa.Column('telegram_respondent_id', sa.Uuid(), nullable=False, comment='Ключ таблицы респондентов с тг. Аналогичное добавление планируется для других источников трафика'),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['telegram_respondent_id'], ['telegram_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица для хранения исследований'
    )
    op.create_table('telegram_respondent__survey',
    sa.Column('telegram_user_id', sa.Uuid(), nullable=False, comment='Ключ таблицы telegram_user'),
    sa.Column('survey_id', sa.Uuid(), nullable=False, comment='Ключ таблицы исследования'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='Дата назначения респондента на исследование'),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['telegram_user_id'], ['telegram_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('telegram_user_id', 'survey_id', 'id'),
    comment='Таблица для хранения респондентов'
    )


def downgrade() -> None:
    op.drop_table('telegram_respondent__survey')
    op.drop_table('survey')
    op.drop_table('telegram_user')
    op.drop_table('role')
    op.drop_table('auth_service')
    op.execute('DROP TYPE rolecodeenum;')
