from typing import TYPE_CHECKING
from uuid import UUID
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import String, ARRAY


from src.database.models.base import Base, create_comment
from src.database.enums import QuestionType

if TYPE_CHECKING:
    from database.models.survey import Survey
    from database.models import WrittenAnswer


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    __table_args__ = create_comment("Таблица для хранения анкеты")

    name: Mapped[str | None]
    survey_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("survey.id")
    )

    survey: Mapped["Survey"] = relationship(back_populates="questionnaires")
    questionnaire_questions: Mapped[list["QuestionnaireQuestion"] | None] = relationship(back_populates="questionnaire")




class QuestionnaireQuestion(Base):
    __tablename__ = "questionnaire_question"
    __table_args__ = create_comment("Таблица для хранения вопросов для анкеты")

    questionnaire_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("questionnaire.id")
    )
    question_text: Mapped[str] = mapped_column(comment="Текст вопроса анкеты")
    number: Mapped[int] = mapped_column(
        comment="Порядковый номер вопроса анкеты"
    )
    choice_text: Mapped[list[str] | None] = mapped_column(
        ARRAY(String),
        default=None,
        comment="Список вопросов для множественного выбора. Зависит от типа",
    )
    written_text: Mapped[str | None] = mapped_column(
        comment="Текст вопроса для письменного ответа. Зависит от типа"
    )
    question_type: Mapped[QuestionType] = mapped_column(comment="Тип вопроса")

    questionnaire: Mapped["Questionnaire"] = relationship(back_populates="questionnaire_questions")
    written_answers: Mapped[list["WrittenAnswer"]] = relationship(
        back_populates="question"
    )
