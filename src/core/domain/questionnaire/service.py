from uuid import UUID

from sqlalchemy.orm import joinedload

from src.core.domain.user.dto import TelegramUserFilterDTO
from src.adapters.api.questionnaire.dto import AssignQuestionnaireDTO
from src.core.domain.user.repository import TelegramUserRepository
from src.lib.paginator import PaginationDTO, PagePaginator, PaginationResultDTO
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)
from sqla_filter import or_unset
from src.database.enums import QuestionType
from src.adapters.api.survey.dto import SurveyUpdateDTO
from src.core.domain.questionnaire.exceptions import (
    QuestionCreateUpdateMismatchError,
    QuestionCreateUpdateQuestionError,
    QuestionnaireCreateUpdateMismatchError,
    QuestionnaireCreateUpdateQuestionError,
)
from src.core.domain.survey.dto import SurveyFilterDTO
from src.database.models import Survey
from src.core.domain.questionnaire.dto import (
    QuestionCreateDTO,
    QuestionFilterDTO,
    QuestionnaireCreateDTO,
    QuestionTextCreateDTO,
    QuestionnaireDTO,
    QuestionnaireFilterDTO,
    RespondentQuestionnaireFilterDTO,
    QuestionUpdateDTO,
)
from src.core.domain.survey.repository import SurveyRepository
from src.core.domain.questionnaire.repository import (
    QuestionnaireRepository,
    QuestionnaireQuestionRepository,
    QuestionTextRepository,
)
from src.core.exceptions import ObjectNotFoundError
from result import Ok, Result, Err


class QuestionnaireService:
    def __init__(
        self,
        questionnaire_repository: QuestionnaireRepository,
        questionnaire_question_repository: QuestionnaireQuestionRepository,
        survey_repository: SurveyRepository,
        question_text_repository: QuestionTextRepository,
        telegram_user_repository: TelegramUserRepository,
        paginator: PagePaginator,
    ) -> None:
        self._questionnaire_repository = questionnaire_repository
        self._questionnaire_question_repository = (
            questionnaire_question_repository
        )
        self._survey_repository = survey_repository
        self._question_text_repository = question_text_repository
        self._telegram_user_repository = telegram_user_repository
        self._paginator = paginator

    async def create(
        self, *, dto: QuestionnaireCreateDTO
    ) -> Result[
        None,
        ObjectNotFoundError
        | QuestionnaireCreateUpdateQuestionError
        | QuestionnaireCreateUpdateMismatchError,
    ]:
        validation_result = self._business_validation(dto)
        if isinstance(validation_result, Err):
            return validation_result
        survey = await self._survey_repository.get(
            filter_=SurveyFilterDTO(
                id=dto.survey_id,
            )
        )
        if survey is None:
            return Err(ObjectNotFoundError(obj=Survey.__name__))
        questionnaire = await self._questionnaire_repository.create(dto)
        number = 1
        for question in dto.questionnaire_questions:
            question.number = number
            await self._questionnaire_question_create(
                questionnaire.id, dto=question
            )
            number += 1
        await self._survey_repository.update(survey, dto=SurveyUpdateDTO())
        return Ok(None)

    async def get_questionnaire_by_id(
        self, questionnaire_id: UUID
    ) -> Result[QuestionnaireDTO, ObjectNotFoundError]:
        questionnaire = await self._questionnaire_repository.get(
            filter_=QuestionnaireFilterDTO(id=questionnaire_id),
            options=(
                joinedload(Questionnaire.questionnaire_questions).options(
                    joinedload(QuestionnaireQuestion.question_texts),
                ),
            ),
        )
        if questionnaire is None:
            return Err(ObjectNotFoundError(obj=Questionnaire.__name__))

        return Ok(QuestionnaireDTO.model_validate(questionnaire))

    async def add_question(
        self, questionnaire_id: UUID, *, dto: QuestionCreateDTO
    ) -> Result[
        QuestionnaireQuestion,
        ObjectNotFoundError
        | QuestionCreateUpdateQuestionError
        | QuestionCreateUpdateMismatchError,
    ]:
        validation_result = self._question_business_validation(question=dto)
        if isinstance(validation_result, Err):
            return validation_result
        questionnaire = await self._questionnaire_repository.get(
            QuestionnaireFilterDTO(id=questionnaire_id)
        )
        if questionnaire is None:
            return Err(ObjectNotFoundError(obj=Questionnaire.__name__))
        max_question_number = (
            await self._questionnaire_question_repository.get_max_number(
                QuestionFilterDTO(questionnaire_id=questionnaire_id)
            )
        )
        dto.number = max_question_number + 1 if max_question_number is not None else 1
        question = await self._questionnaire_question_create(
            questionnaire.id,
            dto=dto,
        )

        return Ok(question)

    async def update_question(
        self,
        question_id: UUID,
        dto: QuestionUpdateDTO,
    ) -> Result[
        QuestionnaireQuestion,
        ObjectNotFoundError,
    ]:
        question = await self._questionnaire_question_repository.get(
            QuestionFilterDTO(id=question_id),
            options=(joinedload(QuestionnaireQuestion.question_texts),),
        )
        if question is None:
            return Err(ObjectNotFoundError(obj=QuestionnaireQuestion.__name__))
        await self._questionnaire_question_repository.update_question(
            model=question, dto=dto
        )
        return Ok(question)

    async def get_assign_list(
        self, pagination_dto: PaginationDTO, *, dto: AssignQuestionnaireDTO
    ) -> PaginationResultDTO[QuestionnaireDTO]:
        user = await self._telegram_user_repository.get(
            filter_=TelegramUserFilterDTO(
                tg_id=dto.tg_id,
            )
        )

        stmt = await self._questionnaire_repository.get_assign_list_stmt(
            filter_=RespondentQuestionnaireFilterDTO(
                telegram_user_id=or_unset(user.id if user else None),
                is_active=or_unset(dto.is_active),
            )
        )
        return await self._paginator.paginate(
            stmt, dto_model=QuestionnaireDTO, pagination=pagination_dto
        )

    async def _questionnaire_question_create(
        self,
        questionnaire_id: UUID,
        *,
        dto: QuestionCreateDTO,
    ) -> QuestionnaireQuestion:
        question = (
            await self._questionnaire_question_repository.create_question(
                questionnaire_id, dto=dto
            )
        )
        if dto.question_type == QuestionType.WRITTEN.value:
            await self._question_text_repository.create_one(
                dto=QuestionTextCreateDTO(
                    questionnaire_question_id=question.id,
                    text=dto.written_text,
                )
            )
        else:
            dtos = [
                QuestionTextCreateDTO(
                    questionnaire_question_id=question.id,
                    text=text,
                )
                for text in dto.choice_text
            ]
            await self._question_text_repository.create_all(dtos)
        return question

    def _question_business_validation(
        self,
        question: QuestionCreateDTO,
    ) -> Result[
        None,
        QuestionCreateUpdateQuestionError | QuestionCreateUpdateMismatchError,
    ]:
        if bool(question.choice_text) == bool(question.written_text):
            return Err(
                QuestionCreateUpdateQuestionError(
                    question_name=question.question_text
                )
            )
        if (
            question.question_type
            in (QuestionType.ONE_CHOICE, QuestionType.MULTIPLE_CHOICE)
            and question.written_text is not None
        ):
            return Err(
                QuestionCreateUpdateMismatchError(
                    question_name=question.question_text
                )
            )
        if (
            question.question_type == QuestionType.WRITTEN
            and question.choice_text is not None
        ):
            return Err(
                QuestionCreateUpdateMismatchError(
                    question_name=question.question_text
                )
            )
        return Ok(None)

    def _business_validation(
        self, dto: QuestionnaireCreateDTO
    ) -> Result[
        None,
        QuestionnaireCreateUpdateQuestionError
        | QuestionnaireCreateUpdateMismatchError,
    ]:
        for question in dto.questionnaire_questions:
            self._question_business_validation(question=question)
        return Ok(None)
