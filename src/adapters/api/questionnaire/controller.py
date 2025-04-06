from http import HTTPStatus
from typing import Any
from uuid import UUID

from src.adapters.api.questionnaire.exceptions import (
    QuestionCreateUpdateHTTPError,
    QuestionnaireCreateUpdateHTTPError,
)
from src.core.domain.questionnaire.exceptions import (
    QuestionCreateUpdateMismatchError,
    QuestionCreateUpdateQuestionError,
    QuestionnaireCreateUpdateQuestionError,
    QuestionnaireCreateUpdateMismatchError,
    QuestionnaireCreateUpdateNumberExistsError,
)
from src.adapters.api.exceptions import (
    ObjectNotFoundHTTPError,
)
from src.adapters.api.questionnaire.schema import (
    CreateQuestionSchema,
    QuestionnaireCreateSchema,
    QuestionnaireGetSchema,
)
from src.core.exceptions import ObjectNotFoundError
from src.core.domain.questionnaire.service import QuestionnaireService
from src.adapters.api.schema import APIDetailSchema
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import Response, post, get
from litestar.controller import Controller
from aioinject import Injected
from aioinject.ext.litestar import inject
from result import Err
from litestar.plugins.htmx import HTMXTemplate
from litestar.response import Template


class QuestionnaireController(Controller):
    path = "/questionnaire"
    tags = ("Questionnaire endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post("/create", status_code=200)
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
                    | QuestionnaireCreateUpdateNumberExistsError()
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

    @post("/add_question", status_code=200)
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
                    message=f"Вопрос `{questionnaire_id}` успешно создан",
                )
            },
            status_code=HTTPStatus.OK,
        )

    @get("/{id:int}", status_code=200)
    @inject
    async def get_questionnaire_id(
        self,
        id: UUID,
        service: Injected[QuestionnaireService],
    ) -> Any:
        result = await service.get_questionnaire_by_id(questionnaire_id=id)
        if isinstance(result, Err):
            raise ObjectNotFoundHTTPError(message=result.err_value.message)
        return QuestionnaireGetSchema.model_validate(result.ok_value)

    @get("/static", exclude_from_auth=True)
    async def get_questionnaire_form(self) -> Template:
        return HTMXTemplate(
            template_name="index.html",
        )
