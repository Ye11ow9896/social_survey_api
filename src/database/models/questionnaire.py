from typing import Any
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, create_comment, uuid_pk


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    __table_args__ = create_comment("Таблица для сохранения структуры анкеты")

    name: Mapped[str | None]
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
