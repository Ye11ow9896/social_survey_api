from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select

from src.core.domain.user.dto import TelegramUserFilterDTO
from src.adapters.api.telegram_user.dto import TelegramUserCreateDTO
from src.database.models import TelegramUser


class TelegramUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    async def get(self, filter_: TelegramUserFilterDTO) -> TelegramUser:
        stmt = select(TelegramUser)
        stmt = filter_.apply(stmt)
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_all_stmt(
        self, filter_: TelegramUserFilterDTO
    ) -> Select[tuple[TelegramUser]]:
        stmt = select(TelegramUser)
        stmt = filter_.apply(stmt)
        return stmt

    # не забыть удалить
    # async def does_user_exists(self, tg_id: int):
    #     stmt = select(TelegramUser).where(TelegramUser.tg_id == tg_id)
    #     return (await self._session.scalars(stmt)).one_or_none()

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
