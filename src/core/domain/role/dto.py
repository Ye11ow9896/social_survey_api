from uuid import UUID

from database.models.role import RoleCodeEnum
from src.core.dto import BaseDTO


class RoleDTO(BaseDTO):
    id: UUID
    name: str
    code: RoleCodeEnum
