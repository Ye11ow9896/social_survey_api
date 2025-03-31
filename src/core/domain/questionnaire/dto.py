import uuid

from typing import Annotated
from pydantic import BeforeValidator
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from src.adapters.api.schema import BaseSchema
from src.database.enums import QuestionType
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)


class QuestionDTO(BaseSchema):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """

    question_text: str
    number: int
    written_text: str | None
    choice_text: list[str] | None
    question_type: Annotated[
        QuestionType, BeforeValidator(lambda type_: QuestionType(type_))
    ]


class QuestionnaireCreateDTO(BaseSchema):
    survey_id: uuid.UUID
    name: str
    questionnaire_questions: Annotated[
        list[QuestionDTO],
        BeforeValidator(
            lambda dtos: [QuestionDTO.model_validate(dto) for dto in dtos]
        ),
    ]


class QuestionnaireFilterDTO(BaseFilter):
    id: Annotated[
        uuid.UUID | Unset,
        FilterField(Questionnaire.id, operator=eq),
    ] = UNSET


class QuestionFilterDTO(BaseFilter):
    id: Annotated[
        str | Unset,
        FilterField(QuestionnaireQuestion.questionnaire_id, operator=eq),
    ] = UNSET
