from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models.role import Role


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def create(self, dto: Any) -> Any:
        ...