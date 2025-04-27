from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.questionnaire import Questionnaire

from src.database.models.owner_survey import OwnerSurvey
from src.database.models.base import Base, create_comment
from src.lib.utils import utc_now
from sqlalchemy import DateTime


if TYPE_CHECKING:
    from src.database.models.user import TelegramUser


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

    questionnaires: Mapped[list[Questionnaire]] = relationship(
        back_populates="survey"
    )
    telegram_respondents: Mapped[list["TelegramUser"] | None] = relationship(
        viewonly=True,
        secondary=OwnerSurvey.__table__,
    )
