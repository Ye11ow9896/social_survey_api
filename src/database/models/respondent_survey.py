from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from src.database.models.base import Base
from src.lib.utils import utc_now


class RespondentSurvey(Base):
    __tablename__ = "respondent__survey"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    survey_id: Mapped[UUID] = mapped_column(
        ForeignKey("survey.id", ondelete="CASCADE"), primary_key=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, onupdate=utc_now
    )
