from typing import Literal
from uuid import UUID

from pydantic import Field

from src.core.domain.questionnaire.dto import (
    QuestionCreateDTO,
    QuestionnaireCreateDTO,
    QuestionDTO,
    UpdateQuestionCreateDTO,
)
from src.adapters.api.schema import BaseSchema


class CreateQuestionSchema(BaseSchema):
    """
    Вопрос.
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - заполняем поле text_answer is not None
    """

    question_text: str = Field(alias="questionText")
    written_text: str | None = Field(alias="writtenText", default=None)
    choice_text: list[str] | None = Field(alias="choiceText", default=None)
    question_type: Literal["written", "multiple_choice", "one_choice"] = Field(
        alias="questionType"
    )

    def to_dto(self) -> QuestionCreateDTO:
        return QuestionCreateDTO(
            question_text=self.question_text,
            written_text=self.written_text,
            choice_text=self.choice_text,
            question_type=self.question_type,
        )
    

class UpdateQuestionSchema(BaseSchema):
    # Немного сомневаюсь в правильности написания классов. Может использовать
    # Field для number? И в UpdateQuestionCreateDTO нужно ли "= None" в полях?
    question_text: str | None = Field(alias="questionText", default=None)
    number: int | None = None

    def to_dto(self) -> UpdateQuestionCreateDTO:
        return UpdateQuestionCreateDTO(
            question_text=self.question_text,
            number=self.number,
        )

class QuestionnaireCreateSchema(BaseSchema):
    survey_id: UUID
    name: str
    questionnaire_questions: list[CreateQuestionSchema]

    def to_dto(self) -> QuestionnaireCreateDTO:
        return QuestionnaireCreateDTO(
            survey_id=self.survey_id,
            name=self.name,
            questionnaire_questions=self.questionnaire_questions,
        )


class QuestionnaireWithQuestionsSchema(BaseSchema):
    survey_id: UUID
    name: str
    questions: list[QuestionDTO]
