from database.models.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_service(self, service_name: str) -> AuthService | None:
        stmt = select(AuthService).where(
            AuthService.service_name == service_name
        )
        return (await self._session.scalars(stmt)).one_or_none()
