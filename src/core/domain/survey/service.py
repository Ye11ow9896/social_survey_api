from sqla_filter import or_unset

from src.core.domain.survey.exceptions import PermissionDeniedForRoleError
from src.core.domain.user.dto import TelegramUserFilterDTO
from src.database.enums import RoleCodeEnum
from src.database.models import TelegramUser
from src.core.domain.user.repository import (
    TelegramUserRepository,
    OwnerSurveyRepository,
)
from src.lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO
from src.core.domain.survey.dto import SurveyFilterDTO
from src.core.domain.survey.repository import SurveyRepository
from src.adapters.api.survey.dto import SurveyCreateDTO
from src.database.models import Survey
from src.core.exceptions import ObjectNotFoundError
from sqlalchemy.orm import joinedload
from result import Err, Ok, Result


class SurveyService:
    def __init__(
        self,
        survey_repository: SurveyRepository,
        paginator: PagePaginator,
        user_repository: TelegramUserRepository,
        owner_survey_repository: OwnerSurveyRepository,
    ) -> None:
        self._survey_repository = survey_repository
        self._paginator = paginator
        self._user_repository = user_repository
        self._owner_survey_repository = owner_survey_repository

    async def create(
        self, dto: SurveyCreateDTO
    ) -> Result[Survey, ObjectNotFoundError | PermissionDeniedForRoleError]:
        user = await self._user_repository.get(
            filter_=TelegramUserFilterDTO(tg_id=dto.tg_id),
            options=(joinedload(TelegramUser.role),),
        )
        if user is None:
            return Err(ObjectNotFoundError(obj=TelegramUser.__name__))
        if user.role.code != RoleCodeEnum.OWNER:
            return Err(
                PermissionDeniedForRoleError(current_role=user.role.code)
            )
        survey = await self._survey_repository.create(dto=dto)
        await self._owner_survey_repository.create(
            id=user.id, survey_id=survey.id
        )
        return Ok(survey)

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
