import enum

from src.core.domain.role.contants import RoleIdConstant


class RoleCodeEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    RESPONDENT = "RESPONDENT"
    OWNER = "OWNER"

    @property
    def identifier(self) -> RoleIdConstant:
        match self:
            case self.ADMIN:
                return RoleIdConstant.ADMIN
            case self.RESPONDENT:
                return RoleIdConstant.RESPONDENT
            case self.OWNER:
                return RoleIdConstant.OWNER


class SexEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class QuestionType(enum.StrEnum):
    """
    Если тип вопроса one_choice или multiple_choice - поле choice_text is not None
    Если тип вопроса written - поле choice_text is None
    """

    WRITTEN = "written"
    MULTIPLE_CHOICE = "multiple_choice"
    ONE_CHOICE = "one_choice"
