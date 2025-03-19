from typing import Any
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import String, ARRAY

from src.database.models.base import Base, create_comment
from src.database.enums import QuestionType


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    __table_args__ = create_comment("Таблица для хранения анкеты")

    question_id: Mapped[UUID | None] = mapped_column(ForeignKey("questionnaire_question.id"), )
    name: Mapped[str | None]

    questionnaire_questions: Mapped[list["QuestionnaireQuestion"] | None] = relationship()

class QuestionnaireQuestion(Base):
    __tablename__ = "questionnaire_question"
    __table_args__ = create_comment("Таблица для хранения вопросов для анкеты")

    question_text: Mapped[str] = mapped_column(comment="Текст вопроса анкеты")
    number: Mapped[int] = mapped_column(comment="Порядковый номер вопроса анкеты")
    choice_text: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None, comment="Список вопросов для множественного выбора. Зависит от типа")
    question_type: Mapped[QuestionType] = mapped_column(comment="Тип вопроса")
