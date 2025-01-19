import enum
from database.models.base import Base
from sqlalchemy.orm import Mapped

class RoleCodeEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    RESPONDENT = "RESPONDENT"


class Role(Base):
    __tablename__ = "user"

    name: Mapped[str]
    code: Mapped[RoleCodeEnum]
