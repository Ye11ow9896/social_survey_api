from uuid import UUID

from pydantic import Field

from src.core.domain.answer.dto import QuestionAnswerCreateUpdateDTO
from src.adapters.api.schema import BaseSchema


class QuestionAnswerCreateSchema(BaseSchema):
    question_id: UUID = Field(alias="questionId")
    tg_id: int = Field(alias="tgId")
    question_text_id: UUID = Field(alias="questionTextId")
    text: str

    def to_dto(self) -> QuestionAnswerCreateUpdateDTO:
        return QuestionAnswerCreateUpdateDTO(
            question_id=self.question_id,
            tg_id=self.tg_id,
            question_text_id=self.question_text_id,
            text=self.text,
        )
