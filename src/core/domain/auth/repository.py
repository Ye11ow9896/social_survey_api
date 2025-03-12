from src.database.models.auth_service import AuthService
from src.database.models.user_admin import UserAdmin
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

    async def get_useradmin(self, username: str) -> UserAdmin | None:
        stmt = select(UserAdmin).where(UserAdmin.username == username)
        return (await self._session.scalars(stmt)).one_or_none()
