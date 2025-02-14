from collections.abc import Sequence

from core.domain.auth.repository import AuthRepository
from core.domain.role.repository import RoleRepository
from database.models.role import Role


class AuthService:
    def __init__(
        self, auth_repository: AuthRepository, role_repository: RoleRepository
    ) -> None:
        self._auth_repository = auth_repository
        self._role_repository = role_repository

    async def test(self) -> Sequence[Role]:
        return await self._role_repository.get_all()
