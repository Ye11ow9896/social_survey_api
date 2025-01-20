from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import (ForeignKey)

from src.database.models.respondent_survey import RespondentSurvey
from src.database.models.base import Base
from src.lib.utils import utc_now

if TYPE_CHECKING:
    from database.models import User

class Survey(Base):
    __tablename__ = "survey"

    respondent_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    description: Mapped[str | None]
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    users: Mapped[list["User"] | None] = relationship(
        viewonly=True,
        secondary=RespondentSurvey.__table__,
    )