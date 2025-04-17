from http import HTTPStatus
from typing import Any, Annotated
from uuid import UUID

from src.core.domain.questionnaire.dto import QuestionnaireDTO
from src.adapters.api.questionnaire.dto import AssignQuestionnaireDTO
from src.core.domain.questionnaire.command import GetQuestionnaireFormCommand
from src.adapters.api.questionnaire.exceptions import (
    QuestionCreateUpdateHTTPError,
    QuestionnaireCreateUpdateHTTPError,
)
from src.core.domain.questionnaire.exceptions import (
    QuestionCreateUpdateMismatchError,
    QuestionCreateUpdateQuestionError,
    QuestionnaireCreateUpdateQuestionError,
    QuestionnaireCreateUpdateMismatchError,
)
from src.adapters.api.exceptions import (
    ObjectNotFoundHTTPError,
)
from src.adapters.api.questionnaire.schema import (
    CreateQuestionSchema,
    QuestionnaireCreateSchema,
    QuestionnaireWithQuestionsSchema,
    UpdateQuestionSchema,
)
from src.lib.paginator import PaginationDTO, PaginationResultDTO
from src.core.exceptions import ObjectNotFoundError
from src.core.domain.questionnaire.service import QuestionnaireService
from src.adapters.api.schema import APIDetailSchema
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import Response, post, get, put
from litestar.controller import Controller
from litestar.response import Template
from litestar.params import Parameter
from aioinject import Injected
from aioinject.ext.litestar import inject
from result import Err


class QuestionnaireController(Controller):
    path = "/questionnaire"
    tags = ("Questionnaire endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post(
        "/create",
        status_code=200,
        description="Создание анкеты с вопросами",
    )
    @inject
    async def create(
        self,
        data: QuestionnaireCreateSchema,
        service: Injected[QuestionnaireService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.create(dto=dto)
        if isinstance(result, Err):
            match exc := result.err_value:
                case ObjectNotFoundError():
                    raise ObjectNotFoundHTTPError(message=exc.message)
                case (
                    QuestionnaireCreateUpdateQuestionError()
                    | QuestionnaireCreateUpdateMismatchError()
                ):
                    raise QuestionnaireCreateUpdateHTTPError(
                        message=exc.message
                    )
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="questionnaire_create_success",
                    message=f"Анкета опроса `{dto.survey_id}` успешно создана",
                )
            },
            status_code=HTTPStatus.OK,
        )

    @post(
        "/add_question",
        status_code=200,
        description="Добавить вопрос к анкете",
    )
    @inject
    async def add_question(
        self,
        questionnaire_id: UUID,
        data: CreateQuestionSchema,
        service: Injected[QuestionnaireService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.add_question(questionnaire_id, dto=dto)
        if isinstance(result, Err):
            match exc := result.err_value:
                case ObjectNotFoundError():
                    raise ObjectNotFoundHTTPError(message=exc.message)
                case (
                    QuestionCreateUpdateQuestionError()
                    | QuestionCreateUpdateMismatchError()
                ):
                    raise QuestionCreateUpdateHTTPError(message=exc.message)
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="questionnaire_create_success",
                    message=f"Вопрос `{result.ok_value.id}` успешно создан",
                )
            },
            status_code=HTTPStatus.OK,
        )

    @get(
        "/{id:str}",
        status_code=200,
        description="Получить анкету со списком вопросов",
    )
    @inject
    async def get_questionnaire_id(
        self,
        id: UUID,
        service: Injected[QuestionnaireService],
    ) -> QuestionnaireWithQuestionsSchema:
        result = await service.get_questionnaire_by_id(questionnaire_id=id)
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return QuestionnaireWithQuestionsSchema(
            survey_id=result.ok_value.survey_id,
            name=result.ok_value.name,
            questions=result.ok_value.questionnaire_questions,
        )

    @get(
        "/static/{id:str}",
        exclude_from_auth=True,
        description="Вывеси форму анкеты",
    )
    @inject
    async def get_questionnaire_form(
        self,
        id: UUID,
        command: Injected[GetQuestionnaireFormCommand],
    ) -> Template:
        result = await command.execute(id)
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return Template(
            template_str=result.ok_value,
        )

    @put(
        "question/{id:str}/update",
        status_code=200,
        description="Обновить вопрос анкеты",
    )
    @inject
    async def update_qestionnaire_question(
        self,
        id: UUID,
        data: UpdateQuestionSchema,
        service: Injected[QuestionnaireService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.update_question(question_id=id, dto=dto)
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="questionnaire_update_success",
                    message=f"Вопрос `{result.ok_value.id}` успешно обновлен",
                )
            },
            status_code=HTTPStatus.OK,
        )

    @get(
        "/assigned/all",
        status_code=200,
        description="Получить список назначенных на респондентов анкет с вопросами",
    )
    @inject
    async def get_questionnaire_assign_list(
        self,
        service: Injected[QuestionnaireService],
        tg_id: Annotated[int | None, Parameter(query="tgId")] = None,
        is_active: Annotated[bool | None, Parameter(query="isActive")] = None,
        page_size: Annotated[
            int, Parameter(ge=1, le=1_000, query="pageSize")
        ] = 100,
        page: Annotated[int, Parameter(ge=1)] = 1,
    ) -> PaginationResultDTO[QuestionnaireDTO]:
        pagination_dto = PaginationDTO(
            page_size=page_size,
            page=page,
        )
        return await service.get_assign_list(
            pagination_dto,
            dto=AssignQuestionnaireDTO(
                tg_id=tg_id,
                is_active=is_active,
            ),
        )
