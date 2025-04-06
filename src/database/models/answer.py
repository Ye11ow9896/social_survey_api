from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from src.database.models.questionnaire import QuestionnaireQuestion
from src.database.models.base import Base, create_comment


class AbstractAnswerModel(Base):
    __abstract__ = True

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("questionnaire_question.id")
    )
    telegram_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("telegram_user.id")
    )


class WrittenAnswer(AbstractAnswerModel):
    __tablename__ = "written_answer"
    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "telegram_user_id",
            name="uq_question_id_telegram_user_id",
        ),
        create_comment("Таблица для хранения ответа на письменный вопрос"),
    )

    text: Mapped[str] = mapped_column(comment="Текст ответа на вопрос")

    question: Mapped[QuestionnaireQuestion] = relationship(
        back_populates="written_answers"
    )


class ChoiceAnswer(AbstractAnswerModel):
    __tablename__ = "choice_answer"
    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "telegram_user_id",
            name="uq_question_id_telegram_user_id_question_text_id",
        ),
        create_comment(
            "Таблица для хранения ответа с выбором(множественным и единственным из нескольких)"
        ),
    )

    question_text_id: Mapped[UUID] = mapped_column(
        ForeignKey("question_text.id")
    )

    question: Mapped[QuestionnaireQuestion] = relationship(
        back_populates="written_answers"
    )
