from result import Result
from sqla_filter import or_unset

from src.core.exceptions import ObjectNotFoundError
from src.core.domain.survey.exceptions import PermissionDeniedForRoleError
from src.core.domain.user.dto import TelegramUserFilterDTO
from src.database.enums import RoleCodeEnum
from src.database.models import TelegramUser
from src.core.domain.user.repository import (
    TelegramUserRepository,
    OwnerSurveyRepository,
)
from src.lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO
from src.core.domain.survey.dto import AssingSurveyDTO, SurveyFilterDTO
from src.core.domain.survey.repository import SurveyRepository
from src.adapters.api.survey.dto import SurveyCreateDTO
from src.database.models import Survey
from src.core.exceptions import ObjectNotFoundError
from sqlalchemy.orm import joinedload
from result import Err, Ok, Result


class SurveyService:
    def __init__(
        self,
        user_repository: TelegramUserRepository,
        survey_repository: SurveyRepository,
        paginator: PagePaginator,
        owner_survey_repository: OwnerSurveyRepository,
    ) -> None:
        self._telegram_user_repository = user_repository
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

    async def get_assign_list(
        self,
        pagination: PaginationDTO,
        *,
        dto: AssingSurveyDTO,
    ) -> PaginationResultDTO:
        user = await self._telegram_user_repository.get(
            filter_=TelegramUserFilterDTO(
                tg_id=dto.tg_id,
            )
        )
        filter_dto = SurveyFilterDTO(
            telegram_user_id=or_unset(user.id if user else None),
            name=or_unset(dto.name),
        )
        stmt = await self._survey_repository.get_assign_list_stmt(filter_=filter_dto)
        return await self._paginator.paginate(stmt, pagination=pagination)
