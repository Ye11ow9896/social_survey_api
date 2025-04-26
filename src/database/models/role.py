from .base import Base, create_comment
from sqlalchemy.orm import Mapped
from ..enums import RoleCodeEnum


class Role(Base):
    __tablename__ = "role"
    __table_args__ = create_comment(
        "Таблица для хранения ролей пользаков. пока роль будет так храниться, создана для возможного расширения функционала ролей"
    )

    name: Mapped[str]
    code: Mapped[RoleCodeEnum]
