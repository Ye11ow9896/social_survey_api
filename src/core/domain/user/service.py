from uuid import UUID
from result import Err, Ok, Result

from sqla_filter import or_unset
from src.adapters.api.telegram_user.dto import (
    TelegramUserCreateDTO,
)
from src.core.exceptions import ObjectAlreadyExistsError, ObjectNotFoundError
from src.core.domain.questionnaire.dto import QuestionnaireFilterDTO
from src.core.domain.questionnaire.repository import QuestionnaireRepository
from src.database.models.questionnaire import Questionnaire
from src.core.domain.user.dto import TelegramUserDTO, TelegramUserFilterDTO
from src.core.domain.user.repository import (
    RespondentQuestionnaireRepository,
    TelegramUserRepository,
)
from src.database.models import TelegramUser
from src.lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO


class TelegramUserService:
    def __init__(
        self,
        user_repository: TelegramUserRepository,
        questionnaire_repository: QuestionnaireRepository,
        respondent_questionnaire_repository: RespondentQuestionnaireRepository,
        paginator: PagePaginator,
    ) -> None:
        self._user_repository = user_repository
        self._questionnaire_repository = questionnaire_repository
        self._respondent_questionnaire_repository = (
            respondent_questionnaire_repository
        )
        self._paginator = paginator

    async def create(
        self, dto: TelegramUserCreateDTO
    ) -> Result[TelegramUser, ObjectAlreadyExistsError]:
        user = await self._user_repository.get(
            filter_=TelegramUserFilterDTO(tg_id=dto.tg_id)
        )
        if user is not None:
            return Err(ObjectAlreadyExistsError(obj=TelegramUser.__name__))
        created_user = await self._user_repository.create(dto=dto)
        return Ok(created_user)

    async def get_all(
        self,
        pagination: PaginationDTO,
        *,
        tg_id: int | None,
        is_bot: bool | None,
    ) -> Result[PaginationResultDTO[TelegramUserDTO], ObjectNotFoundError]:
        filter_dto = TelegramUserFilterDTO(
            tg_id=or_unset(tg_id),
            is_bot=or_unset(is_bot),
        )
        stmt = await self._user_repository.get_all_stmt(filter_=filter_dto)
        result = await self._paginator.paginate(
            stmt, dto_model=TelegramUserDTO, pagination=pagination
        )
        if not result.items:
            return Err(ObjectNotFoundError(obj=TelegramUser.__name__))
        return Ok(result)

    async def appoint_questionnaire_to_user(
        self,
        tg_id: int,
        questionnaire_id: UUID,
    ) -> Result[None, ObjectNotFoundError]:
        user = await self._user_repository.get(
            filter_=TelegramUserFilterDTO(tg_id=tg_id)
        )
        questionnaire = await self._questionnaire_repository.get(
            filter_=QuestionnaireFilterDTO(id=questionnaire_id)
        )
        if user is None:
            return Err(ObjectNotFoundError(obj=TelegramUser.__name__))
        if questionnaire is None:
            return Err(ObjectNotFoundError(obj=Questionnaire.__name__))
        created_resp_quest = (
            await self._respondent_questionnaire_repository.create(
                user.id, questionnaire_id
            )
        )
        return Ok(created_resp_quest)
