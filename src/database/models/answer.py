from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.database.models.questionnaire import QuestionnaireQuestion
from src.database.models.base import Base, create_comment


class AbstractAnswerModel(Base):
    __abstract__ = True

    question_id: Mapped[UUID] = mapped_column(ForeignKey("questionnaire.id"))
    telegram_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("questionnaire.id")
    )


class WrittenAnswer(AbstractAnswerModel):
    __tablename__ = "written_answer"
    __table_args__ = create_comment(
        "Таблица для хранения ответа на письменный вопрос"
    )

    text: Mapped[str] = mapped_column(comment="Текст ответа на вопрос")

    question: Mapped[QuestionnaireQuestion] = relationship()
