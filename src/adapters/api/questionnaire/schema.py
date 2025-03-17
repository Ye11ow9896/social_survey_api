from typing import Literal

from pydantic import Field

from core.domain.questionnaire.dto import QuestionnaireCreateDTO
from src.adapters.api.schema import BaseSchema



class QuestionSchema(BaseSchema):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """
    question_text: str = Field(alias="questionText")
    written_text: str | None = Field(alias="writtenText", default=None)
    choice_text: list[str] | None = Field(alias="choiceText", default=None)
    question_type: Literal["written", "multiple_choice", "one_choice"] = Field(alias="questionType")


class QuestionnaireSchema(BaseSchema):
    description: str
    questions: list[QuestionSchema]


class QuestionnaireCreateSchema(BaseSchema):
    name: str
    questionnaire: QuestionnaireSchema

    def to_dto(self) -> QuestionnaireCreateDTO:
        return QuestionnaireCreateDTO(
            name=self.name,
            data=self.questionnaire,
        )
