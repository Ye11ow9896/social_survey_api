from uuid import UUID
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from src.core.domain.questionnaire.dto import (
    QuestionFilterDTO,
    QuestionnaireCreateDTO,
    QuestionDTO,
    QuestionnaireFilterDTO,
)
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)


class QuestionnaireRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(
        self,
        filter_: QuestionnaireFilterDTO,
        options: Sequence[ExecutableOption] | None = None,
    ) -> Questionnaire:
        stmt = select(Questionnaire)
        stmt = filter_.apply(stmt)
        stmt = stmt.options(*options or ())
        return (await self._session.scalars(stmt)).one_or_none()

    async def create(self, dto: QuestionnaireCreateDTO) -> Questionnaire:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    def _build_model(self, dto: QuestionnaireCreateDTO) -> Questionnaire:
        return Questionnaire(name=dto.name)


class QuestionnaireQuestionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(
        self,
        filter_: QuestionFilterDTO,
        options: Sequence[ExecutableOption] | None = None,
    ) -> QuestionnaireQuestion:
        stmt = select(QuestionnaireQuestion)
        stmt = filter_.apply(stmt)
        stmt = stmt.options(*options or ())
        return (await self._session.scalars(stmt)).one_or_none()

    async def create_question(
        self,
        questionnaire_id: UUID,
        dto: QuestionDTO,
    ) -> QuestionnaireQuestion:
        model = self._build_model(dto=dto, questionnaire_id=questionnaire_id)
        self._session.add(model)
        await self._session.flush()
        return model

    async def create_questions(
        self, questionnaire_id: UUID, *, dtos: list[QuestionDTO]
    ) -> None:
        models = []
        for dto in dtos:
            models.append(
                self._build_model(dto=dto, questionnaire_id=questionnaire_id)
            )
        self._session.add_all(models)
        await self._session.flush()

    def _build_model(
        self,
        questionnaire_id: UUID,
        dto: QuestionDTO,
    ) -> QuestionnaireQuestion:
        return QuestionnaireQuestion(
            questionnaire_id=questionnaire_id,
            question_text=dto.question_text,
            number=dto.number,
            choice_text=dto.choice_text,
            written_text=dto.written_text,
            question_type=dto.question_type,
        )
