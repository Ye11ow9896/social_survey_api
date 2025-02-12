from uuid import UUID

from adapters.api.schema import BaseSchema
from database.models.role import RoleCodeEnum


class RoleSchema(BaseSchema):
    id: UUID
    name: str
    code: RoleCodeEnum
