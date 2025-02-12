from uuid import UUID

from core.dto import BaseDTO
from database.models.role import RoleCodeEnum


class RoleDTO(BaseDTO):
    id: UUID
    name: str
    code: RoleCodeEnum
