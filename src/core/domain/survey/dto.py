from typing import Annotated
from uuid import UUID

from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from src.database.models import Survey


class SurveyFilterDTO(BaseFilter):
    id: Annotated[
        UUID | Unset,
        FilterField(Survey.id, operator=eq),
    ] = UNSET
