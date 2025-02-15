from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from .respondent_survey import RespondentSurvey
from .base import Base, create_comment
from src.lib.utils import utc_now


if TYPE_CHECKING:
    from .user import TelegramUser


class Survey(Base):
    __tablename__ = "survey"
    __table_args__ = create_comment("Таблица для хранения исследований")

    telegram_respondent_id: Mapped[UUID] = mapped_column(
        ForeignKey("telegram_user.id"),
        comment="Ключ таблицы респондентов с тг. Аналогичное добавление планируется для других источников трафика",
    )
    name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    description: Mapped[str | None]
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, onupdate=utc_now
    )

    telegram_respondents: Mapped[list["TelegramUser"] | None] = relationship(
        viewonly=True,
        secondary=RespondentSurvey.__table__,
    )
