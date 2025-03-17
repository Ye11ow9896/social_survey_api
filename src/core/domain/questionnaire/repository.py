from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.domain.questionnaire.dto import QuestionnaireCreateDTO
from core.domain.role.dto import RoleFilterDTO
from database.models import TelegramUser
from database.models.questionnaire import Questionnaire
from src.database.models.role import Role


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
            name=dto.name,
            data=dto.data.model_dump(mode="json")
        )