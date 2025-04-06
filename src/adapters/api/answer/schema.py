from uuid import UUID

from pydantic import Field

from src.core.domain.answer.dto import QuestionAnswerCreateDTO
from src.adapters.api.schema import BaseSchema


class QuestionAnswerCreateSchema(BaseSchema):
    question_id: UUID = Field(alias="questionId")
    telegram_user_id: UUID = Field(alias="telegramUserId")
    question_text_id: UUID = Field(alias="questionTextId")
    text: str | None

    def to_dto(self) -> QuestionAnswerCreateDTO:
        return QuestionAnswerCreateDTO(
            question_id=self.question_id,
            telegram_user_id=self.telegram_user_id,
            question_text_id=self.question_text_id,
            text=self.text,
        )
