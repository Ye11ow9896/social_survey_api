from dataclasses import dataclass
from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq, icontains_op

from src.lib.base_model import AppBaseModel
from src.database.models.owner_survey import RespondentSurvey
from src.database.models import Survey


class SurveyDTO(AppBaseModel):
    id: UUID
    name: str | None
    created_at: datetime
    description: str | None
    updated_at: datetime


class SurveyFilterDTO(BaseFilter):
    id: Annotated[
        str | Unset,
        FilterField(Survey.id, operator=eq),
    ] = UNSET
    tg_uuid: Annotated[
        str | Unset,
        FilterField(RespondentSurvey.telegram_user_id, operator=eq),
    ] = UNSET
    name: Annotated[
        str | Unset,
        FilterField(Survey.name, operator=icontains_op),
    ] = UNSET


@dataclass(frozen=True, slots=True)
class AssingSurveyDTO:
    tg_id: int | None = None
    name: str | None = None