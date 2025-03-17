from http import HTTPStatus
from typing import Any

from adapters.api.questionnaire.schema import QuestionnaireCreateSchema
from src.adapters.api.schema import APIDetailSchema
from src.adapters.api.survey.schema import SurveyCreateSchema
from src.core.domain.survey.service import SurveyService
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import Response, post
from litestar.controller import Controller
from aioinject import Injected
from aioinject.ext.litestar import inject


class QuestionnaireController(Controller):
    path = "/questionnaire"
    tags = ("Questionnaire endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post("/create", status_code=200)
    @inject
    async def create(
        self,
        data: QuestionnaireCreateSchema,
        service: Injected[SurveyService],
    ) -> Response[Any]:
        dto = data.to_dto()
        await service.create(dto)
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