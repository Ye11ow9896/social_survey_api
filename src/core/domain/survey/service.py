from sqla_filter import or_unset

from src.lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO
from src.core.domain.survey.dto import SurveyFilterDTO
from src.core.domain.survey.repository import SurveyRepository
from src.adapters.api.survey.dto import SurveyCreateDTO
from src.database.models import Survey


class SurveyService:
    def __init__(
        self,
        user_repository: SurveyRepository,
        paginator: PagePaginator,
    ) -> None:
        self._survey_repository = user_repository
        self._paginator = paginator

    async def create(self, dto: SurveyCreateDTO) -> Survey:
        new_survey = await self._survey_repository.create(dto=dto)
        return new_survey

    async def get_all(
        self,
        pagination: PaginationDTO,
        name: str | None,
    ) -> PaginationResultDTO:
        filter_dto = SurveyFilterDTO(
            name=or_unset(name),
        )
        stmt = await self._survey_repository.get_all_stmt(filter_=filter_dto)
        return await self._paginator.paginate(stmt, pagination=pagination)
