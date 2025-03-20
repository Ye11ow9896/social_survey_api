from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.domain.role.dto import RoleFilterDTO
from src.database.models import TelegramUser
from src.database.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Sequence[Role]:
        stmt = select(Role)
        return (await self._session.scalars(stmt)).all()

    async def get(
        self,
        filter_: RoleFilterDTO,
    ) -> Role:
        stmt = select(Role).join(TelegramUser, TelegramUser.role_id == Role.id)
        stmt = filter_.apply(stmt)
        return (await self._session.scalars(stmt)).one_or_none()
