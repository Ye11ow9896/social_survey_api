import uuid
from dataclasses import dataclass

from typing import Annotated
from pydantic import BeforeValidator
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from src.core.dto import BaseDTO
from src.database.enums import QuestionType
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)


class QuestionCreateDTO(BaseDTO):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """

    question_text: str
    number: int | None
    written_text: str | None
    choice_text: list[str] | None
    question_type: Annotated[
        QuestionType, BeforeValidator(lambda type_: QuestionType(type_))
    ]


class QuestionnaireCreateDTO(BaseDTO):
    survey_id: uuid.UUID
    name: str
    question_text: str
    questionnaire_questions: Annotated[
        list[QuestionCreateDTO],
        BeforeValidator(
            lambda dtos: [
                QuestionCreateDTO.model_validate(dto) for dto in dtos
            ]
        ),
    ]


class QuestionDTO(BaseDTO):
    id: uuid.UUID
    number: int
    question_type: Annotated[
        QuestionType, BeforeValidator(lambda type_: QuestionType(type_))
    ]
    question_text: str
    question_texts: Annotated[
        list[str],
        BeforeValidator(lambda models: [model.text for model in models]),
    ]


class QuestionnaireDTO(BaseDTO):
    survey_id: uuid.UUID
    name: str
    questionnaire_questions: Annotated[
        list[QuestionDTO],
        BeforeValidator(
            lambda models: QuestionDTO.model_validate_list(models)
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
        FilterField(QuestionnaireQuestion.id, operator=eq),
    ] = UNSET
    questionnaire_id: Annotated[
        uuid.UUID | Unset,
        FilterField(QuestionnaireQuestion.questionnaire_id, operator=eq),
    ] = UNSET


@dataclass(frozen=True, slots=True)
class QuestionTextCreateDTO:
    questionnaire_question_id: uuid.UUID
    text: str
