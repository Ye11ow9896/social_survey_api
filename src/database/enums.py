import enum
from uuid import UUID

from src.core.domain.role.contants import RoleIdConstant


class RoleCodeEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    RESPONDENT = "RESPONDENT"

    @property
    def identifier(self) -> UUID:
        match self:
            case self.ADMIN:
                return RoleIdConstant.ADMIN
            case self.RESPONDENT:
                return RoleIdConstant.RESPONDENT

class SexEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
