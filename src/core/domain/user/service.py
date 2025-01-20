from typing import Any

from core.domain.user.repository import UserRepository


class UserService:
    def __init__(
            self,
            user_repository: UserRepository
    ) -> None:
        self._repository = user_repository

    async def create(self, dto: Any) -> Any:
        return await self._repository.create(dto)
