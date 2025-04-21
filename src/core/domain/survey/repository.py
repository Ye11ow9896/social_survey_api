from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select
from sqlalchemy.sql.base import ExecutableOption

from src.core.domain.survey.dto import SurveyFilterDTO
from src.database.models.survey import Survey
from src.adapters.api.survey.dto import SurveyCreateDTO, SurveyUpdateDTO


class SurveyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(
        self,
        filter_: SurveyFilterDTO,
        options: Sequence[ExecutableOption] | None = None,
    ) -> Survey:
        stmt = select(Survey)
        stmt = filter_.apply(stmt)
        stmt = stmt.options(*options or ())
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_all_stmt(
        self, filter_: SurveyFilterDTO
    ) -> Select[tuple[Survey]]:
        stmt = select(Survey)
        stmt = filter_.apply(stmt)
        return stmt

    async def create(self, dto: SurveyCreateDTO) -> Survey:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    async def update(self, model: Survey, *, dto: SurveyUpdateDTO) -> Survey:
        assigned_model = self._assign_model(model, dto=dto)
        self._session.add(assigned_model)
        await self._session.flush()
        return assigned_model

    def _build_model(self, dto: SurveyCreateDTO) -> Survey:
        return Survey(
            name=dto.name,
            description=dto.description,
        )

    def _assign_model(self, model: Survey, *, dto: SurveyUpdateDTO) -> Survey:
        if dto.name is not None:
            model.name = dto.name
        if dto.description is not None:
            model.description = dto.description
        return model
