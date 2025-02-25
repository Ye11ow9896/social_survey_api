from litestar import Response
from adapters.api.schema import APIDetailSchema
from http import HTTPStatus
from typing import Any

from core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import get
from litestar.controller import Controller


class CommonController(Controller):
    path = "/common"
    tags = ("Common endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @get("/health-check", status_code=200, exclude_from_auth=True)
    async def health_check(self) -> Response[Any]:
        return Response(
            content={
                "detail": APIDetailSchema(
                    status_code=HTTPStatus.OK,
                    code="health_check_ok",
                    message="Успешный ответ сервера",
                )
            },
            status_code=HTTPStatus.OK,
        )

