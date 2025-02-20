from adapters.api.telegram_user.dto import TelegramUserCreateDTO, TelegramUserFilterDTO
from core.domain.user.repository import TelegramUserRepository
from database.models import TelegramUser
from lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO


class TelegramUserService:
    def __init__(
        self,
        user_repository: TelegramUserRepository,
        paginator: PagePaginator,
    ) -> None:
        self._repository = user_repository
        self._paginator = paginator

    async def create(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        new_user = await self._repository.create(dto=dto)
        return new_user

    async def get_all(
        self,
        filter_dto: TelegramUserFilterDTO,
        *,
        pagination: PaginationDTO
    ) -> PaginationResultDTO:
        stmt = await self._repository.get_all_stmt(filter_=filter_dto)
        return await self._paginator.paginate(stmt, pagination=pagination)

