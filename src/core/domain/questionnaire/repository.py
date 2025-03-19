from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.questionnaire.dto import QuestionnaireCreateDTO, QuestionDTO
from src.database.models.questionnaire import Questionnaire, QuestionnaireQuestion


class QuestionnaireRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: QuestionnaireCreateDTO) -> Questionnaire:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    def _build_model(self, dto: QuestionnaireCreateDTO) -> Questionnaire:
        return Questionnaire(
            name=dto.name
        )

class QuestionnaireQuestionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_questions(
        self,
        questionnaire_id: UUID,
        *,
        dtos: list[QuestionDTO]
    ) -> None:
        models = [
            QuestionnaireQuestion(
                questionnaire_id=questionnaire_id,
                question_text=dto.question_text,
                number=dto.number,
                choice_text=dto.choice_text,
                written_text=dto.written_text,
                question_type=dto.question_type,
            )
            for dto in dtos
        ]
        self._session.add_all(models)
        await self._session.flush()




