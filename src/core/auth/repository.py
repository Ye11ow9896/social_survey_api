from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: Any) -> Any:
        model = {1: 1}
        self._session.add(model)
        await self._session.flush()
        return model