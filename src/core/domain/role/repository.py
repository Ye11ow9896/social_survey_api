from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self) -> Sequence[Role]:
        stmt = select(Role)
        return (await self._session.scalars(stmt)).all()
