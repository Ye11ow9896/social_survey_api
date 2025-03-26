from typing import Literal

from pydantic import Field

from src.core.domain.questionnaire.dto import QuestionDTO, QuestionnaireCreateDTO
from src.adapters.api.schema import BaseSchema


class CreateQuestionSchema(BaseSchema):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """

    question_text: str = Field(alias="questionText")
    number: int
    written_text: str | None = Field(alias="writtenText", default=None)
    choice_text: list[str] | None = Field(alias="choiceText", default=None)
    question_type: Literal["written", "multiple_choice", "one_choice"] = Field(
        alias="questionType"
    )

    def to_dto(self) -> QuestionDTO:
        return QuestionDTO(
            question_text=self.question_text,
            number=self.number,
            written_text=self.written_text,
            choice_text=self.choice_text,
            question_type=self.question_type,
        )


class QuestionnaireCreateSchema(BaseSchema):
    name: str
    questionnaire_questions: list[CreateQuestionSchema]

    def to_dto(self) -> QuestionnaireCreateDTO:
        return QuestionnaireCreateDTO(
            name=self.name,
            questionnaire_questions=self.questionnaire_questions,
        )
