from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, create_comment, uuid_pk


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    __table_args__ = create_comment(
        "Таблица для сохранения структуры анкеты"
    )

    id: Mapped[uuid_pk]
    name: Mapped[str | None]
    data: Mapped[dict] = mapped_column(JSON)
