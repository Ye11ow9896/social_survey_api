from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, create_comment
from src.lib.utils import utc_now


class OwnerSurvey(Base):
    __tablename__ = "telegram_owner__survey"
    __table_args__ = create_comment("Таблица для хранения респондентов")

    telegram_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("telegram_user.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Ключ таблицы telegram_user",
    )
    survey_id: Mapped[UUID] = mapped_column(
        ForeignKey("survey.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Ключ таблицы исследования",
    )
    created_at: Mapped[datetime] = mapped_column(
        default=utc_now,
        onupdate=utc_now,
        comment="Дата назначения респондента на исследование",
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)
