from src.core.domain.answer.exceptions import WrittenAnswerCreateTypeError
from src.database.enums import QuestionType
from src.core.domain.user.dto import TelegramUserFilterDTO
from src.core.domain.user.repository import TelegramUserRepository
from src.database.models import TelegramUser, WrittenAnswer
from src.core.domain.answer.dto import (
    WrittenAnswerCreateDTO,
    WrittenAnswerFilterDTO,
)
from src.core.domain.answer.repository import WrittenAnswerRepository
from src.database.models.questionnaire import QuestionnaireQuestion

from src.core.domain.questionnaire.dto import QuestionFilterDTO

from src.core.domain.questionnaire.repository import (
    QuestionnaireQuestionRepository,
)
from src.core.exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from result import Ok, Result, Err


class AnswerService:
    def __init__(
        self,
        repository: WrittenAnswerRepository,
        telegram_user_repository: TelegramUserRepository,
        question_repository: QuestionnaireQuestionRepository,
    ) -> None:
        self._repository = repository
        self._telegram_user_repository = telegram_user_repository
        self._question_repository = question_repository

    async def written_answer_create(
        self, dto: WrittenAnswerCreateDTO
    ) -> Result[
        WrittenAnswer,
        ObjectNotFoundError
        | ObjectAlreadyExistsError
        | WrittenAnswerCreateTypeError,
    ]:
        telegram_user = await self._telegram_user_repository.get(
            filter_=TelegramUserFilterDTO(id=dto.telegram_user_id)
        )
        if telegram_user is None:
            return Err(
                ObjectNotFoundError(
                    obj=TelegramUser.__name__, field=str(dto.telegram_user_id)
                )
            )

        question = await self._question_repository.get(
            filter_=QuestionFilterDTO(id=dto.question_id)
        )
        if question is None:
            return Err(
                ObjectNotFoundError(
                    obj=QuestionnaireQuestion.__name__,
                    field=str(dto.question_id),
                )
            )

        if question.question_type != QuestionType.WRITTEN.value:
            return Err(
                WrittenAnswerCreateTypeError(
                    question_id=dto.question_id,
                    current_type=question.question_type,
                )
            )

        answer_db = await self._repository.get(
            filter_=WrittenAnswerFilterDTO(
                question_id=dto.question_id,
                telegram_user_id=dto.telegram_user_id,
            )
        )
        if answer_db is not None:
            return Err(ObjectAlreadyExistsError(obj=WrittenAnswer.__name__))

        answer = await self._repository.create(dto=dto)
        return Ok(answer)

    async def multiple_choice_answer_create(self):
        ...