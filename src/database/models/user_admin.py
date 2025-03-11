import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, create_comment


class UserAdmin(Base):
    __tablename__ = "user_admin"
    __table_args__ = create_comment(
        "Таблица для авторицации с паролем и пользователем"
    )

    username: Mapped[uuid.UUID]
    hashed_password: Mapped[str] = mapped_column(String(16))
