from litestar import Response
from src.adapters.api.schema import APIDetailSchema
from http import HTTPStatus
from typing import Any

from src.core.domain.auth.middleware import CheckAccessTokenMiddleware
from litestar import get
from litestar.controller import Controller


class CommonController(Controller):
    path = "/common"
    tags = ("Common endpoints",)
    middleware = [CheckAccessTokenMiddleware]

    @get(
        "/health-check",
        status_code=200,
        exclude_from_auth=True,
        description="Проверка работоспособности системы",
    )
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
