from http import HTTPStatus
from typing import Any, assert_never

from src.core.domain.answer.service import AnswerService
from src.adapters.api.answer.schema import QuestionAnswerCreateSchema
from src.adapters.api.exceptions import (
    ObjectNotFoundHTTPError,
    ObjectAlreadyExistsHTTPError,
)

from src.core.exceptions import ObjectNotFoundError, ObjectAlreadyExistsError
from src.adapters.api.schema import APIDetailSchema
from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import Response, post
from litestar.controller import Controller
from aioinject import Injected
from aioinject.ext.litestar import inject
from result import Err


class AnswerController(Controller):
    path = "/answer"
    tags = ("Answer endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @post("/question-answer/create", status_code=200)
    @inject
    async def written_answer_create(
        self,
        data: QuestionAnswerCreateSchema,
        service: Injected[AnswerService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.create(dto=dto)
        if isinstance(result, Err):
            match exc := result.err_value:
                case ObjectNotFoundError():
                    raise ObjectNotFoundHTTPError(message=exc.message)
                case ObjectAlreadyExistsError():
                    raise ObjectAlreadyExistsHTTPError(message=exc.message)
                case _ as never:
                    assert_never(never)

        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="written_answer_create_success",
                    message=f"Ответ на вопрос `{dto.question_id}` успешно создан",
                )
            },
            status_code=HTTPStatus.OK,
        )
