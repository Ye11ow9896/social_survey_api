from datetime import datetime

from src.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

from src.lib.utils import utc_now


class User(Base):
    __tablename__ = "user"

    login: Mapped[str]
    first_name: Mapped[str | None]
    second_name: Mapped[str | None]
    hash_password: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)
