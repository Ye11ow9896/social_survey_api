from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy import select

from src.database.models import WrittenAnswer
from src.core.domain.answer.dto import (
    WrittenAnswerCreateDTO,
    WrittenAnswerFilterDTO,
)


class WrittenAnswerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(
        self,
        filter_: WrittenAnswerFilterDTO,
        options: Sequence[ExecutableOption] | None = None,
    ) -> WrittenAnswer:
        stmt = select(WrittenAnswer)
        stmt = filter_.apply(stmt)
        stmt = stmt.options(*options or ())
        return (await self._session.scalars(stmt)).one_or_none()

    async def create(self, dto: WrittenAnswerCreateDTO) -> WrittenAnswer:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    def _build_model(self, dto: WrittenAnswerCreateDTO) -> WrittenAnswer:
        return WrittenAnswer(
            question_id=dto.question_id,
            telegram_user_id=dto.telegram_user_id,
            text=dto.text,
        )
