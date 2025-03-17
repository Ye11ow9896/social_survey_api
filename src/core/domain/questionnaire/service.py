from uuid import UUID

from src.adapters.api.survey.dto import SurveyUpdateDTO
from src.core.domain.questionnaire.enum import QuestionType
from src.core.domain.questionnaire.exceptions import (
    QuestionnaireCreateUpdateMismatchError,
    QuestionnaireCreateUpdateQuestionError,
)
from src.core.domain.survey.dto import SurveyFilterDTO
from src.database.models import Survey
from src.core.domain.questionnaire.dto import QuestionnaireCreateDTO
from src.core.domain.survey.repository import SurveyRepository
from src.core.domain.questionnaire.repository import QuestionnaireRepository
from src.core.exceptions import ObjectNotFoundError
from result import Ok, Result, Err


class QuestionnaireService:
    def __init__(
        self,
        questionnaire_repository: QuestionnaireRepository,
        survey_repository: SurveyRepository,
    ) -> None:
        self._questionnaire_repository = questionnaire_repository
        self._survey_repository = survey_repository

    async def create(
        self, survey_id: UUID, *, dto: QuestionnaireCreateDTO
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
                id=survey_id,
            )
        )
        if survey is None:
            return Err(ObjectNotFoundError(obj=Survey.__name__))
        if survey.questionnaire_id is not None:
            ...  # Добавить обработку already exists
        questionnaire = await self._questionnaire_repository.create(dto)
        await self._survey_repository.update(
            survey, dto=SurveyUpdateDTO(questionnaire_id=questionnaire.id)
        )
        return Ok(None)

    def _business_validation(
        self, dto: QuestionnaireCreateDTO
    ) -> Result[
        None,
        QuestionnaireCreateUpdateQuestionError
        | QuestionnaireCreateUpdateMismatchError,
    ]:
        for question in dto.data.questions:
            if bool(question.choice_text) == bool(question.written_text):
                return Err(
                    QuestionnaireCreateUpdateQuestionError(
                        question_name=question.question_text
                    )
                )
            if (
                question.question_type
                in (QuestionType.ONE_CHOICE, QuestionType.MULTIPLE_CHOICE)
                and question.written_text is not None
            ):
                return Err(
                    QuestionnaireCreateUpdateMismatchError(
                        question_name=question.question_text
                    )
                )
            if (
                question.question_type == QuestionType.WRITTEN
                and question.choice_text is not None
            ):
                return Err(
                    QuestionnaireCreateUpdateMismatchError(
                        question_name=question.question_text
                    )
                )

        return Ok(None)
