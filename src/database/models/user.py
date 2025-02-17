from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID


from src.database.models.survey import Survey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.database.models.base import Base, create_comment
from src.lib.utils import utc_now
from src.database.models.role import Role

if TYPE_CHECKING:
    from database.models.respondent_survey import RespondentSurvey


class AbstractUserModel(Base):
    """
    Модель пользаков(респондентов) из различных источников трафика с дефолтными полями.
    Такие поля должны содержаться во всех пользовательских таблицах.
    """

    __abstract__ = True

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id"))
    age: Mapped[int | None]
    sex: Mapped[int | None]
    real_first_name: Mapped[str | None]
    real_middle_name: Mapped[str | None]
    real_last_name: Mapped[str | None]
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, onupdate=utc_now
    )


class TelegramUser(AbstractUserModel):
    __tablename__ = "telegram_user"
    __table_args__ = create_comment(
        "Таблица для хранения пользаков из телеграма"
    )

    tg_id: Mapped[int] = mapped_column(
        comment="Идентификатор в тг. в aiogram - id"
    )
    username: Mapped[str | None] = mapped_column(
        comment="Акк в тг. Одноименно переменной в aiogram"
    )
    first_name: Mapped[str | None] = mapped_column(
        comment="first_name. Одноименно переменной в aiogram"
    )
    last_name: Mapped[str | None] = mapped_column(
        comment="last_name. Одноименно переменной в aiogram"
    )
    url: Mapped[str] = mapped_column(
        "Cсылка типа tg://user?id=54763794. Одноименно переменной в aiogram"
    )
    is_bot: Mapped[bool] = mapped_column(
        comment="Одноименно переменной в aiogram"
    )
    is_premium: Mapped[bool] = mapped_column(
        comment="Одноименно переменной в aiogram"
    )

    role: Mapped["Role"] = relationship()
    #surveys: Mapped[list["Survey"] | None] = relationship(
    #    viewonly=True,
    #    secondary=RespondentSurvey.__table__,
    #)
