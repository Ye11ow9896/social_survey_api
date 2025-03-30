from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.questionnaire import Questionnaire

from .respondent_survey import RespondentSurvey
from .base import Base, create_comment
from src.lib.utils import utc_now
from sqlalchemy import DateTime, ForeignKey


if TYPE_CHECKING:
    from .user import TelegramUser


class Survey(Base):
    __tablename__ = "survey"
    __table_args__ = create_comment("Таблица для хранения исследований")

    name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    description: Mapped[str | None]
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    questionnaire: Mapped[Questionnaire | None] = relationship()
    telegram_respondents: Mapped[list["TelegramUser"] | None] = relationship(
        viewonly=True,
        secondary=RespondentSurvey.__table__,
    )
