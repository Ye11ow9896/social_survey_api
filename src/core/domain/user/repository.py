from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select
from src.adapters.api.telegram_user.dto import (
    TelegramUserCreateDTO,
    TelegramUserFilterDTO,
)
from src.database.models import TelegramUser


class TelegramUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    async def get_all_stmt(
        self, filter_: TelegramUserFilterDTO
    ) -> Select[tuple[TelegramUser]]:
        stmt = select(TelegramUser)
        return filter_.apply(stmt)

    def _build_model(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        return TelegramUser(
            role_id=dto.role_id,
            url=dto.url,
            is_bot=dto.is_bot,
            is_premium=dto.is_premium,
            age=dto.age,
            sex=dto.sex,
            real_first_name=dto.real_first_name,
            real_middle_name=dto.real_middle_name,
            real_last_name=dto.real_last_name,
            tg_id=dto.tg_id,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )
