from dataclasses import dataclass
from typing import Annotated
from uuid import UUID
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from database.models import WrittenAnswer


@dataclass(frozen=True, slots=True)
class WrittenAnswerCreateDTO:
    question_id: UUID
    telegram_user_id: UUID
    text: str


class WrittenAnswerFilterDTO(BaseFilter):
    id: Annotated[
        str | Unset,
        FilterField(WrittenAnswer.id, operator=eq),
    ] = UNSET
    question_id: Annotated[
        UUID | Unset,
        FilterField(WrittenAnswer.question_id, operator=eq),
    ] = UNSET
    telegram_user_id: Annotated[
        UUID | Unset,
        FilterField(WrittenAnswer.telegram_user_id, operator=eq),
    ] = UNSET
