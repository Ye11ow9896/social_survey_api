from result import Result
from sqla_filter import or_unset

from src.core.exceptions import ObjectNotFoundError
from src.core.domain.user.repository import TelegramUserRepository
from src.lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO
from src.core.domain.survey.dto import SurveyFilterDTO
from src.core.domain.survey.repository import SurveyRepository
from src.adapters.api.survey.dto import SurveyCreateDTO
from src.database.models import Survey


class SurveyService:
    def __init__(
        self,
        user_repository: TelegramUserRepository,
        survey_repository: SurveyRepository,
        paginator: PagePaginator,
    ) -> None:
        self._user_repository = user_repository
        self._survey_repository = survey_repository
        self._paginator = paginator

    async def create(self, dto: SurveyCreateDTO) -> Survey:
        new_survey = await self._survey_repository.create(dto=dto)
        return new_survey

    async def get_all(
        self,
        pagination: PaginationDTO,
        tg_id: int | None,
        name: str | None,
    ) -> PaginationResultDTO:
        if tg_id is not None:
            user = await self._user_repository
        filter_dto = SurveyFilterDTO(
            tg_id=or_unset(user.id),
            name=or_unset(name),
        )
        stmt = await self._survey_repository.get_all_stmt(filter_=filter_dto)
        return await self._paginator.paginate(stmt, pagination=pagination)
