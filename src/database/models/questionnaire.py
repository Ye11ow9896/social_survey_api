from typing import TYPE_CHECKING
from uuid import UUID
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey


from src.database.models.base import Base, create_comment
from src.database.enums import QuestionType

if TYPE_CHECKING:
    from database.models import QuestionAnswer
    from src.database.models.survey import Survey


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    __table_args__ = create_comment("Таблица для хранения анкеты")

    name: Mapped[str | None]
    survey_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("survey.id")
    )

    survey: Mapped["Survey"] = relationship(back_populates="questionnaires")
    questionnaire_questions: Mapped[list["QuestionnaireQuestion"] | None] = (
        relationship(back_populates="questionnaire")
    )


class QuestionnaireQuestion(Base):
    __tablename__ = "questionnaire_question"
    __table_args__ = create_comment("Таблица для хранения вопросов для анкеты")

    questionnaire_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("questionnaire.id")
    )
    number: Mapped[int] = mapped_column(
        comment="Порядковый номер вопроса анкеты"
    )

    question_type: Mapped[QuestionType] = mapped_column(comment="Тип вопроса")
    question_texts: Mapped[list["QuestionText"]] = relationship(
        back_populates="question"
    )
    question_answers: Mapped[list["QuestionAnswer"]] = relationship(
        back_populates="question"
    )
    questionnaire: Mapped["Questionnaire"] = relationship(
        back_populates="questionnaire_questions"
    )

    @property
    def get_text_list(self) -> list[str]:
        return [question_text.text for question_text in self.question_texts]


class QuestionText(Base):
    __tablename__ = "question_text"
    __table_args__ = create_comment(
        "Таблица для хранения текста вопроса анкеты"
    )

    questionnaire_question_id: Mapped[UUID] = mapped_column(
        ForeignKey("questionnaire_question.id")
    )
    text: Mapped[str]

    question: Mapped[QuestionnaireQuestion] = relationship(
        back_populates="question_texts"
    )
