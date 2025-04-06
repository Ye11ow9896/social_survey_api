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


class QuestionAnswer(AbstractAnswerModel):
    __tablename__ = "question_answer"
    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "telegram_user_id",
            name="uq_question_id_user_id_question_text_id",
        ),
        create_comment(
            "Таблица для хранения ответа на вопрос"
        ),
    )

    question_text_id: Mapped[UUID] = mapped_column(
        ForeignKey("question_text.id")
    )
    text: Mapped[str | None] = mapped_column(default=None, comment="Заполняется только для текстового ответа")

    question: Mapped[QuestionnaireQuestion] = relationship(back_populates="question_answers")