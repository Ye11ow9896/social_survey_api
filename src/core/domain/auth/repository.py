from src.database.models.auth_service import AuthService
from src.database.models.user_admin import UserAdmin
from src.adapters.api.auth.schema import UserAdminSchema
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

    async def get_useradmin_by_username(self, username) -> UserAdminSchema:
        stmt = select(UserAdmin).where(
            UserAdmin.username == username
        )
        return (await self._session.scalars(stmt)).one_or_none() 