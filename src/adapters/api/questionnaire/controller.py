from http import HTTPStatus
from typing import Any
from uuid import UUID

from src.adapters.api.questionnaire.exceptions import (
    QuestionnaireCreateUpdateHTTPError,
)
from src.core.domain.questionnaire.exceptions import (
    QuestionnaireCreateUpdateQuestionError,
    QuestionnaireCreateUpdateMismatchError,
)
from src.adapters.api.exceptions import ObjectNotFoundHTTPError
from src.adapters.api.questionnaire.schema import QuestionnaireCreateSchema
from src.core.exceptions import ObjectNotFoundError
from src.core.domain.questionnaire.service import QuestionnaireService
from src.adapters.api.schema import APIDetailSchema
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import Response, post
from litestar.controller import Controller
from aioinject import Injected
from aioinject.ext.litestar import inject
from result import Err


class QuestionnaireController(Controller):
    path = "/questionnaire"
    tags = ("Questionnaire endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post("/create", status_code=200)
    @inject
    async def create(
        self,
        survey_id: UUID,
        data: QuestionnaireCreateSchema,
        service: Injected[QuestionnaireService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.create(survey_id, dto=dto)
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
                    code="survey_create_success",
                    message="Опрос создан успешно",
                )
            },
            status_code=HTTPStatus.OK,
        )
