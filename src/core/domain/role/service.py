from src.core.domain.role.dto import RoleDTO, RoleFilterDTO
from src.core.domain.role.repository import RoleRepository
from src.core.exceptions import ObjectNotFoundError
from src.database.models import TelegramUser
from result import Ok, Result, Err

class RoleService:
    def __init__(
        self,
        repository: RoleRepository,
    ) -> None:
        self._repository = repository

    async def get_role_by_user(
        self,
        tg_id: int,
    ) -> Result[RoleDTO, ObjectNotFoundError]:
        role = await self._repository.get(
            RoleFilterDTO(tg_id=tg_id)
        )
        if role is None:
            return Err(ObjectNotFoundError(obj=TelegramUser.__name__))

        return Ok(
            RoleDTO(
                name=role.name,
                code=role.code,
            )
        )