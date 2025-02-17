from adapters.api.telegram_user.dto import TelegramUserCreateDTO
from core.domain.user.repository import TelegramUserRepository
from database.models import TelegramUser


class TelegramUserService:
    def __init__(
        self,
        user_repository: TelegramUserRepository,
    ) -> None:
        self._repository = user_repository

    async def create(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        new_user = await self._repository.create(dto=dto)
        return new_user
