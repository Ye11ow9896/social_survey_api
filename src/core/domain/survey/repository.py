from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.survey import Survey
from src.adapters.api.survey.dto import SurveyCreateDTO


class SurveyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: SurveyCreateDTO) -> Survey:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    def _build_model(self, dto: SurveyCreateDTO) -> Survey:
        return Survey(
            name=dto.name,
            description=dto.description,
        )
