from typing import Any, Annotated
from pydantic import BeforeValidator

from adapters.api.schema import BaseSchema

class QuestionnaireOptionsDTO(BaseSchema):
    """
    Набор опций вопроса.
    is_choice_radiobutton - опция вопроса выбор из предложенных ответов
    is_text_answer - текстовый ответ пользователя
    """
    is_choice_radiobutton: bool
    is_text_answer: bool

class QuestionDTO(BaseSchema):
    """
    Вопрос.
    Если установлена опция is_choice_radiobutton - заполняем поле radio_button_answer_choices
    Если установлена опция is_text_answer - заполняем поле text_answer
    """
    question_text: str
    text_answer: str | None
    radio_button_answer_choices: list[str] | None
    options: Annotated[QuestionnaireOptionsDTO, BeforeValidator(lambda dto: QuestionnaireOptionsDTO.model_validate(dto))]

class QuestionnaireDataDTO(BaseSchema):
    description: str
    questions: Annotated[list[QuestionDTO], BeforeValidator(lambda dtos: [QuestionDTO.model_validate(dto) for dto in dtos])]

class QuestionnaireCreateDTO(BaseSchema):
    name: str
    data: Annotated[QuestionnaireDataDTO, BeforeValidator(lambda dto: QuestionnaireDataDTO.model_validate(dto))]