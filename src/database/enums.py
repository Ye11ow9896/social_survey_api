import enum

from src.core.domain.role.contants import RoleIdConstant


class RoleCodeEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    RESPONDENT = "RESPONDENT"

    def get_id(self) -> RoleIdConstant:
        match self:
            case self.ADMIN:
                return RoleIdConstant.ADMIN
            case self.RESPONDENT:
                return RoleIdConstant.RESPONDENT

class SexEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
