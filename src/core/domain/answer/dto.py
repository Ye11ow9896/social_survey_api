from dataclasses import dataclass
from typing import Annotated
from uuid import UUID
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from src.database.models import QuestionAnswer


@dataclass(frozen=True, slots=True)
class QuestionAnswerCreateUpdateDTO:
    question_id: UUID
    tg_id: int
    question_text_id: UUID
    text: str


@dataclass(frozen=True, slots=True)
class QuestionAnswerCreateDTO:
    question_id: UUID
    telegram_user_id: int
    question_text_id: UUID
    text: str


class QuestionAnswerFilterDTO(BaseFilter):
    id: Annotated[
        str | Unset,
        FilterField(QuestionAnswer.id, operator=eq),
    ] = UNSET
    question_id: Annotated[
        UUID | Unset,
        FilterField(QuestionAnswer.question_id, operator=eq),
    ] = UNSET
    telegram_user_id: Annotated[
        UUID | Unset,
        FilterField(QuestionAnswer.telegram_user_id, operator=eq),
    ] = UNSET
    question_text_id: Annotated[
        UUID | Unset,
        FilterField(QuestionAnswer.question_text_id, operator=eq),
    ] = UNSET
