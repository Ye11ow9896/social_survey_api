from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, create_comment
from src.lib.utils import utc_now
from sqlalchemy import DateTime



class RespondentQuestionnaire(Base):
    __tablename__ = "telegram_respondent__questionnaire"
    __table_args__ = create_comment(
        "Таблица для хранения назначенных анкет на респондентов"
    )

    telegram_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("telegram_user.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Ключ таблицы telegram_user",
    )
    questionnaire_id: Mapped[UUID] = mapped_column(
        ForeignKey("questionnaire.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Ключ таблицы анкет",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        comment="Дата назначения анкеты на респондента",
    )
    is_active: Mapped[bool] = mapped_column(default=True)
