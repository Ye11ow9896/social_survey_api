from src.core.domain.survey.repository import SurveyRepository
from src.adapters.api.survey.dto import SurveyCreateDTO
from src.database.models import Survey

class SurveyService:
    def __init__(
        self,
        user_repository: SurveyRepository,
    ) -> None:
        self._repository = user_repository

    async def create(self, dto: SurveyCreateDTO) -> Survey:
        new_survey = await self._repository.create(dto=dto)
        return new_survey