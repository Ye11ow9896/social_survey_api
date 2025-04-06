from http import HTTPStatus
from typing import Any, assert_never

from src.adapters.api.answer.exceptions import WrittenAnswerCreateTypeHTTPError
from src.core.domain.answer.exceptions import WrittenAnswerCreateTypeError
from src.core.domain.answer.service import AnswerService
from src.adapters.api.answer.schema import WrittenAnswerCreateSchema
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

    @post("/written-answer/create", status_code=200)
    @inject
    async def written_answer_create(
        self,
        data: WrittenAnswerCreateSchema,
        service: Injected[AnswerService],
    ) -> Response[Any]:
        dto = data.to_dto()
        result = await service.written_answer_create(dto=dto)
        if isinstance(result, Err):
            match exc := result.err_value:
                case ObjectNotFoundError():
                    raise ObjectNotFoundHTTPError(message=exc.message)
                case ObjectAlreadyExistsError():
                    raise ObjectAlreadyExistsHTTPError(message=exc.message)
                case WrittenAnswerCreateTypeError():
                    raise WrittenAnswerCreateTypeHTTPError(message=exc.message)
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


    @post("/multiple-choice/create", status_code=200)
    @inject
    async def multiple_choice_answer_create(
        self,
        service: Injected[AnswerService],
    ):
        ...