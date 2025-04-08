from uuid import UUID

from sqlalchemy.orm import joinedload

from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)
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
    QuestionCreateDTO,
    QuestionDTO,
    QuestionnaireCreateDTO,
    QuestionTextCreateDTO,
    QuestionnaireDTO,
    QuestionnaireFilterDTO,
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
    ) -> None:
        self._questionnaire_repository = questionnaire_repository
        self._questionnaire_question_repository = (
            questionnaire_question_repository
        )
        self._survey_repository = survey_repository
        self._question_text_repository = question_text_repository

    async def create(
        self, *, dto: QuestionnaireCreateDTO
    ) -> Result[
        None,
        ObjectNotFoundError
        | QuestionnaireCreateUpdateQuestionError
        | QuestionnaireCreateUpdateMismatchError
        | QuestionnaireCreateUpdateNumberExistsError,
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
        for question in dto.questionnaire_questions:
            await self._questionnaire_question_create(
                questionnaire.id, dto=question
            )
        await self._survey_repository.update(survey, dto=SurveyUpdateDTO())
        return Ok(None)

    async def get_questionnaire_by_id(
        self, questionnaire_id: UUID
    ) -> Result[QuestionnaireDTO, ObjectNotFoundError]:
        questionnaire = await self._questionnaire_repository.get(
            filter_=QuestionnaireFilterDTO(id=questionnaire_id),
            options=(joinedload(Questionnaire.questionnaire_questions).options(
            joinedload(QuestionnaireQuestion.question_texts),),
        ))
        if questionnaire is None:
            return Err(ObjectNotFoundError(obj=Questionnaire.__name__))
        questionnaire_questions = [
            QuestionDTO(
                id=question.id,
                number=question.number,
                question_type=question.question_type,
                text=[qt.text for qt in question.question_texts]
            )
            for question in questionnaire.questionnaire_questions
        ]

        return Ok(
            QuestionnaireDTO(
                survey_id=questionnaire.survey_id,
                name=questionnaire.name,
                questionnaire_questions=questionnaire_questions,
            )
        )
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
        question = await self._questionnaire_question_create(
            questionnaire.id, dto=dto
        )

        return Ok(question)

    async def _questionnaire_question_create(
        self, questionnaire_id: UUID, *, dto: QuestionCreateDTO
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
        | QuestionnaireCreateUpdateMismatchError
        | QuestionnaireCreateUpdateNumberExistsError,
    ]:
        exists_numbers = []
        for question in dto.questionnaire_questions:
            if question.number in exists_numbers:
                return Err(
                    QuestionnaireCreateUpdateNumberExistsError(question.id)
                )
            self._question_business_validation(question=question)
            exists_numbers.append(question.number)
        return Ok(None)
