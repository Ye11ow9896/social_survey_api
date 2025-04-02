from uuid import UUID

from pydantic import Field

from src.core.domain.answer.dto import WrittenAnswerCreateDTO
from src.adapters.api.schema import BaseSchema


class WrittenAnswerCreateSchema(BaseSchema):
    question_id: UUID = Field(alias="questionId")
    telegram_user_id: UUID = Field(alias="telegramUserId")
    text: str

    def to_dto(self) -> WrittenAnswerCreateDTO:
        return WrittenAnswerCreateDTO(
            question_id=self.question_id,
            telegram_user_id=self.telegram_user_id,
            text=self.text,
        )
