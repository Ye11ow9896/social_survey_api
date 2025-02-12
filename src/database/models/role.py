import enum
from .base import Base
from sqlalchemy.orm import Mapped

class RoleCodeEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    RESPONDENT = "RESPONDENT"


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str]
    code: Mapped[RoleCodeEnum]
