from typing import Annotated
from pydantic import BeforeValidator

from src.adapters.api.schema import BaseSchema
from src.database.enums import QuestionType


class QuestionDTO(BaseSchema):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """

    question_text: str
    written_text: str | None
    choice_text: list[str] | None
    question_type: Annotated[
        QuestionType, BeforeValidator(lambda type_: QuestionType(type_))
    ]


class QuestionnaireDataDTO(BaseSchema):
    description: str
    questions: Annotated[
        list[QuestionDTO],
        BeforeValidator(
            lambda dtos: [QuestionDTO.model_validate(dto) for dto in dtos]
        ),
    ]


class QuestionnaireCreateDTO(BaseSchema):
    name: str
    data: Annotated[
        QuestionnaireDataDTO,
        BeforeValidator(lambda dto: QuestionnaireDataDTO.model_validate(dto)),
    ]
