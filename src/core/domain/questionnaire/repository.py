from uuid import UUID
from typing import Sequence

from sqlalchemy import func, select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.orm import joinedload

from src.core.domain.questionnaire.dto import (
    QuestionFilterDTO,
    QuestionUpdateDTO,
    QuestionnaireCreateDTO,
    QuestionCreateDTO,
    QuestionnaireFilterDTO,
    QuestionTextCreateDTO,
    RespondentQuestionnaireFilterDTO,
)
from src.database.models import RespondentQuestionnaire
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
    QuestionText,
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
        return (await self._session.scalars(stmt)).unique().one_or_none()

    async def create(self, dto: QuestionnaireCreateDTO) -> Questionnaire:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    async def get_assign_list_stmt(
        self, filter_: RespondentQuestionnaireFilterDTO
    ) -> Select[tuple[Questionnaire]]:
        stmt = select(Questionnaire).join(
            RespondentQuestionnaire,
            RespondentQuestionnaire.questionnaire_id == Questionnaire.id,
        )
        stmt = filter_.apply(stmt)
        return stmt.options(
            joinedload(Questionnaire.questionnaire_questions).options(
                joinedload(QuestionnaireQuestion.question_texts)
            )
        )

    def _build_model(self, dto: QuestionnaireCreateDTO) -> Questionnaire:
        return Questionnaire(name=dto.name, survey_id=dto.survey_id)


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
        return (await self._session.scalars(stmt)).unique().one_or_none()

    async def get_max_number(
        self,
        filter_: QuestionFilterDTO,
        options: Sequence[ExecutableOption] | None = None,
    ) -> int | None:
        stmt = select(func.max(QuestionnaireQuestion.number))
        stmt = filter_.apply(stmt)
        stmt = stmt.options(*options or ())
        return (await self._session.scalars(stmt)).one_or_none()

    async def create_question(
        self,
        questionnaire_id: UUID,
        dto: QuestionCreateDTO,
    ) -> QuestionnaireQuestion:
        model = self._build_model(dto=dto, questionnaire_id=questionnaire_id)
        self._session.add(model)
        await self._session.flush()
        return model

    async def create_questions(
        self, questionnaire_id: UUID, *, dtos: list[QuestionCreateDTO]
    ) -> None:
        models = []
        for dto in dtos:
            models.append(
                self._build_model(dto=dto, questionnaire_id=questionnaire_id)
            )
        self._session.add_all(models)
        await self._session.flush()

    async def update_question(
        self, model: QuestionnaireQuestion, dto: QuestionUpdateDTO
    ) -> QuestionnaireQuestion:
        assigned_model = self._assign_model(model=model, dto=dto)
        self._session.add(assigned_model)
        await self._session.flush()
        return assigned_model

    @staticmethod
    def _assign_model(
        model: QuestionnaireQuestion, dto: QuestionUpdateDTO
    ) -> QuestionnaireQuestion:
        if dto.question_text is not None:
            model.question_text = dto.question_text
        if dto.number is not None:
            model.number = dto.number
        return model

    def _build_model(
        self,
        questionnaire_id: UUID,
        dto: QuestionCreateDTO,
    ) -> QuestionnaireQuestion:
        return QuestionnaireQuestion(
            questionnaire_id=questionnaire_id,
            question_text=dto.question_text,
            number=dto.number,
            question_type=dto.question_type,
        )


class QuestionTextRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_one(self, dto: QuestionTextCreateDTO) -> None:
        model = self._build_model(dto=dto)
        self._session.add(model)
        await self._session.flush()

    async def create_all(self, dtos: list[QuestionTextCreateDTO]) -> None:
        models = [self._build_model(dto=dto) for dto in dtos]
        self._session.add_all(models)
        await self._session.flush()

    def _build_model(self, dto: QuestionTextCreateDTO) -> QuestionText:
        return QuestionText(
            questionnaire_question_id=dto.questionnaire_question_id,
            text=dto.text,
        )
