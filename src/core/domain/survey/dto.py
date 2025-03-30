from datetime import datetime
from typing import Annotated

from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq, ilike_op

from src.lib.base_model import AppBaseModel
from src.database.models import Survey


class SurveyDTO(AppBaseModel):
    name: str | None
    created_at: datetime
    description: str | None
    updated_at: datetime


class SurveyFilterDTO(BaseFilter):
    id: Annotated[
        str | Unset,
        FilterField(Survey.id, operator=eq),
    ] = UNSET
    name: Annotated[
        str | Unset,
        FilterField(Survey.name, operator=ilike_op),
    ] = UNSET
