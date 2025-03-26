from uuid import UUID

from src.database.models.questionnaire import Questionnaire
from src.database.enums import QuestionType
from src.adapters.api.survey.dto import SurveyUpdateDTO
from src.core.domain.questionnaire.exceptions import (
    QuestionCreateUpdateMismatchError,
    QuestionCreateUpdateQuestionError,
    QuestionnaireCreateUpdateMismatchError,
    QuestionnaireCreateUpdateQuestionError,
    QuestionnaireCreateUpdateNumberExistsError,
)
from src.core.domain.survey.dto import SurveyFilterDTO
from src.database.models import Survey
from src.core.domain.questionnaire.dto import (
    QuestionDTO,
    QuestionnaireCreateDTO,
    QuestionnaireFilterDTO,
)
from src.core.domain.survey.repository import SurveyRepository
from src.core.domain.questionnaire.repository import (
    QuestionnaireRepository,
    QuestionnaireQuestionRepository,
)
from src.core.exceptions import ObjectAlreadyExistsError, ObjectNotFoundError
from result import Ok, Result, Err


class QuestionnaireService:
    def __init__(
        self,
        questionnaire_repository: QuestionnaireRepository,
        questionnaire_question_repository: QuestionnaireQuestionRepository,
        survey_repository: SurveyRepository,
    ) -> None:
        self._questionnaire_repository = questionnaire_repository
        self._questionnaire_question_repository = (
            questionnaire_question_repository
        )
        self._survey_repository = survey_repository

    async def create(
        self, survey_id: UUID, *, dto: QuestionnaireCreateDTO
    ) -> Result[
        None,
        ObjectNotFoundError
        | ObjectAlreadyExistsError
        | QuestionnaireCreateUpdateQuestionError
        | QuestionnaireCreateUpdateMismatchError
        | QuestionnaireCreateUpdateNumberExistsError,
    ]:
        validation_result = self._business_validation(dto)
        if isinstance(validation_result, Err):
            return validation_result
        survey = await self._survey_repository.get(
            filter_=SurveyFilterDTO(
                id=survey_id,
            )
        )
        if survey is None:
            return Err(ObjectNotFoundError(obj=Survey.__name__))
        if survey.questionnaire_id is not None:
            return Err(ObjectAlreadyExistsError(obj=Questionnaire.__name__))
        questionnaire = await self._questionnaire_repository.create(dto)
        await self._questionnaire_question_repository.create_questions(
            questionnaire.id, dtos=dto.questionnaire_questions
        )
        await self._survey_repository.update(
            survey, dto=SurveyUpdateDTO(questionnaire_id=questionnaire.id)
        )
        return Ok(None)

    async def create_question(
        self, questionnaire_id: UUID, *, dto: QuestionDTO
    ) -> Result[
        None,
        ObjectNotFoundError
        | ObjectAlreadyExistsError
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
        await self._questionnaire_question_repository.create_question(
            questionnaire.id, dto=dto
        )
        return Ok(None)

    def _question_business_validation(
        self,
        question: QuestionDTO,
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
        | QuestionnaireCreateUpdateMismatchError
        | QuestionnaireCreateUpdateNumberExistsError,
    ]:
        exists_numbers = []
        for question in dto.questionnaire_questions:
            if question.number in exists_numbers:
                return Err(
                    QuestionnaireCreateUpdateNumberExistsError(
                        question.written_text
                    )
                )
            self._question_business_validation(question=question)
            exists_numbers.append(question.number)
        return Ok(None)
