from datetime import datetime, timezone
from typing import Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select
from sqlalchemy.sql.base import ExecutableOption

from src.database.models.role import Role
from src.database.models import OwnerSurvey
from src.core.domain.user.dto import TelegramUserFilterDTO
from src.adapters.api.telegram_user.dto import TelegramUserCreateDTO
from src.database.models.respondent_questionnaire import (
    RespondentQuestionnaire,
)
from src.database.models import TelegramUser


class TelegramUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        model = self._build_model(dto)
        self._session.add(model)
        await self._session.flush()
        return model

    async def get(
        self,
        filter_: TelegramUserFilterDTO,
        options: Sequence[ExecutableOption] | None = None,
    ) -> TelegramUser:
        stmt = select(TelegramUser)
        stmt = filter_.apply(stmt)
        stmt = stmt.options(*options or ())
        return (await self._session.scalars(stmt)).one_or_none()

    async def get_all_stmt(
        self, filter_: TelegramUserFilterDTO
    ) -> Select[tuple[TelegramUser]]:
        stmt = select(TelegramUser).join(
            Role,
            Role.id == TelegramUser.role_id,
        )
        stmt = filter_.apply(stmt)
        return stmt

    def _build_model(self, dto: TelegramUserCreateDTO) -> TelegramUser:
        return TelegramUser(
            role_id=dto.role_id,
            url=dto.url,
            is_bot=dto.is_bot,
            is_premium=dto.is_premium,
            age=dto.age,
            sex=dto.sex,
            real_first_name=dto.real_first_name,
            real_middle_name=dto.real_middle_name,
            real_last_name=dto.real_last_name,
            tg_id=dto.tg_id,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )


class RespondentQuestionnaireRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self, id: UUID, questionnaire_id: UUID
    ) -> RespondentQuestionnaire:
        model = self._build_model(id, questionnaire_id)
        self._session.add(model)
        await self._session.flush()
        return model

    def _build_model(
        self, id: UUID, questionnaire_id: UUID
    ) -> RespondentQuestionnaire:
        return RespondentQuestionnaire(
            telegram_user_id=id,
            questionnaire_id=questionnaire_id,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            is_active=True,
        )


class OwnerSurveyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, id: UUID, survey_id: UUID) -> OwnerSurvey:
        model = self._build_model(id, survey_id)
        self._session.add(model)
        await self._session.flush()
        return model

    def _build_model(self, id: UUID, survey_id: UUID) -> OwnerSurvey:
        return OwnerSurvey(
            telegram_user_id=id,
            survey_id=survey_id,
        )
