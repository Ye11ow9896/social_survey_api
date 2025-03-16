from src.adapters.api.telegram_user.dto import (
    TelegramUserCreateDTO,
)
from sqla_filter import or_unset

from src.core.domain.user.dto import TelegramUserDTO, TelegramUserFilterDTO
from src.core.domain.user.repository import TelegramUserRepository
from src.database.models import TelegramUser
from src.lib.paginator import PagePaginator, PaginationResultDTO, PaginationDTO


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
        pagination: PaginationDTO,
        *,
        tg_id: int | None,
        is_bot: bool | None,
    ) -> PaginationResultDTO[TelegramUserDTO]:
        filter_dto = TelegramUserFilterDTO(
            tg_id=or_unset(tg_id),
            is_bot=or_unset(is_bot),
        )
        stmt = await self._repository.get_all_stmt(filter_=filter_dto)
        return await self._paginator.paginate(
            stmt, dto_model=TelegramUserDTO, pagination=pagination
        )
