from typing import Annotated

from pydantic import Field

from adapters.api.survey.dto import SurveyCreateDTO
from core.domain.questionnaire.dto import QuestionnaireCreateDTO
from src.adapters.api.schema import BaseSchema

class QuestionnaireOptionsSchema(BaseSchema):
    is_choice_radiobutton: bool = Field(alias="isChoiceRadiobutton", default=False)
    is_text_answer: bool = Field(alias="isTextAnswer", default=False)


class QuestionSchema(BaseSchema):
    question_text: str = Field(alias="questionText")
    text_answer: str | None = Field(alias="textAnswer", default=None)
    radio_button_answer_choices: list[str] | None = Field(alias="radioButtonAnswerChoices", default=None)
    options: QuestionnaireOptionsSchema


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
