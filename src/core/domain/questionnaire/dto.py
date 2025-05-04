import uuid
from dataclasses import dataclass

from typing import Annotated
from pydantic import BeforeValidator
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from src.database.models import RespondentQuestionnaire
from src.core.dto import BaseDTO
from src.database.enums import QuestionType
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion, QuestionText,
)


class QuestionCreateDTO(BaseDTO):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """

    question_text: str
    number: int | None = None
    written_text: str | None
    choice_text: list[str] | None
    question_type: Annotated[
        QuestionType, BeforeValidator(lambda type_: QuestionType(type_))
    ]


class QuestionUpdateDTO(BaseDTO):
    question_text: str | None
    number: int | None


class QuestionnaireCreateDTO(BaseDTO):
    survey_id: uuid.UUID
    name: str
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


class QuestionTextDTO(BaseDTO):
    id: uuid.UUID
    questionnaire_question_id: uuid.UUID
    text: str


class QuestionWithAnswerDTO(BaseDTO):
    id: uuid.UUID
    number: int
    question_type: Annotated[
        QuestionType, BeforeValidator(lambda type_: QuestionType(type_))
    ]
    question_text: str
    question_texts: Annotated[
        list[QuestionTextDTO],
        BeforeValidator(
            lambda models: QuestionTextDTO.model_validate_list(models)
        ),
    ]
    question_answers: Annotated[
        list[str],
        BeforeValidator(
            lambda models: [model.text for model in models if model.text]
        ),
    ]


class QuestionnaireDTO(BaseDTO):
    id: uuid.UUID
    survey_id: uuid.UUID
    name: str
    questionnaire_questions: Annotated[
        list[QuestionWithAnswerDTO],
        BeforeValidator(
            lambda models: QuestionWithAnswerDTO.model_validate_list(models)
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


class RespondentQuestionnaireFilterDTO(BaseFilter):
    telegram_user_id: Annotated[
        uuid.UUID | Unset,
        FilterField(RespondentQuestionnaire.telegram_user_id, operator=eq),
    ] = UNSET
    is_active: Annotated[
        bool | Unset,
        FilterField(RespondentQuestionnaire.is_active, operator=eq),
    ] = UNSET
    questionnaire_id: Annotated[
        uuid.UUID | Unset,
        FilterField(RespondentQuestionnaire.questionnaire_id, operator=eq),
    ] = UNSET


class QuestionTextFilterDTO(BaseFilter):
    id: Annotated[
        uuid.UUID | Unset,
        FilterField(QuestionText.id, operator=eq),
    ] = UNSET

