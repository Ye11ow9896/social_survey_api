from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.database.models.respondent_survey import RespondentSurvey
from src.database.models.base import Base
from src.lib.utils import utc_now
from src.database.models.role import Role

if TYPE_CHECKING:
    from database.models.survey import Survey


class User(Base):
    __tablename__ = "user"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id"))
    login: Mapped[str]
    first_name: Mapped[str | None]
    second_name: Mapped[str | None]
    hash_password: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, onupdate=utc_now
    )

    role: Mapped["Role"] = relationship()
    surveys: Mapped[list["Survey"] | None] = relationship(
        viewonly=True,
        secondary=RespondentSurvey.__table__,
    )
