from sqlalchemy.orm import joinedload

from src.core.domain.answer.exceptions import AnswerOneChoiceCreateError
from src.database.enums import QuestionType
from src.core.domain.answer.repository import QuestionAnswerRepository
from src.database.models import QuestionAnswer
from src.core.domain.user.dto import TelegramUserFilterDTO
from src.core.domain.user.repository import TelegramUserRepository
from src.database.models import TelegramUser
from src.core.domain.answer.dto import (
    QuestionAnswerCreateUpdateDTO,
    QuestionAnswerFilterDTO, QuestionAnswerCreateDTO,
)
from src.database.models.questionnaire import QuestionnaireQuestion, QuestionText

from src.core.domain.questionnaire.dto import QuestionFilterDTO, QuestionTextFilterDTO

from src.core.domain.questionnaire.repository import (
    QuestionnaireQuestionRepository, QuestionTextRepository,
)
from src.core.exceptions import ObjectNotFoundError
from result import Ok, Result, Err


class AnswerService:
    def __init__(
        self,
        repository: QuestionAnswerRepository,
        telegram_user_repository: TelegramUserRepository,
        question_repository: QuestionnaireQuestionRepository,
        question_text_repository: QuestionTextRepository,
    ) -> None:
        self._repository = repository
        self._telegram_user_repository = telegram_user_repository
        self._question_repository = question_repository
        self._question_text_repository = question_text_repository

    async def create_update(
        self, dto: QuestionAnswerCreateUpdateDTO
    ) -> Result[
        QuestionAnswer,
        ObjectNotFoundError
        | AnswerOneChoiceCreateError,
    ]:
        telegram_user = await self._telegram_user_repository.get(
            filter_=TelegramUserFilterDTO(tg_id=dto.tg_id)
        )
        if telegram_user is None:
            return Err(
                ObjectNotFoundError(
                    obj=TelegramUser.__name__, field=str(dto.telegram_user_id)
                )
            )

        question = await self._question_repository.get(
            filter_=QuestionFilterDTO(id=dto.question_id),
            options=(joinedload(QuestionnaireQuestion.question_answers),)
        )
        if question is None:
            return Err(
                ObjectNotFoundError(
                    obj=QuestionnaireQuestion.__name__,
                    field=str(dto.question_id),
                )
            )
        question_text = self._question_text_repository.get(
            filter_=QuestionTextFilterDTO(id=dto.question_text_id)
        )
        if question_text is None:
            return Err(
                ObjectNotFoundError(
                    obj=QuestionText.__name__,
                    field=str(dto.question_text_id),
                )
            )

        answer_db = await self._repository.get(
            filter_=QuestionAnswerFilterDTO(
                question_id=dto.question_id,
                telegram_user_id=telegram_user.id,
                question_text_id=dto.question_text_id
            )
        )
        if answer_db is not None:
            return Ok(await self._repository.update(answer_db, text=dto.text))
        else:
            if question.question_type == QuestionType.ONE_CHOICE and question.question_answers:
                return Err(AnswerOneChoiceCreateError())
            result = await self._repository.create(
                dto=QuestionAnswerCreateDTO(
                    question_id=dto.question_id,
                    telegram_user_id=telegram_user.id,
                    question_text_id=dto.question_text_id,
                    text=dto.text
                )
            )
            return Ok(result)
