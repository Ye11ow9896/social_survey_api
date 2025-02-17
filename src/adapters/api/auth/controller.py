from typing import assert_never, Annotated

from adapters.api.auth.exceptions import (
    UnauthorizedHTTPError,
    TokenCreateHTTPError,
)
from core.domain.auth.dto import LoginCredentialsDTO
from core.domain.auth.exceptions import BadPasswordError, TokenEncodeError
from core.domain.auth.service import AuthenticationService
from core.exceptions import ObjectNotFoundError

from litestar import post
from litestar.controller import Controller
from litestar.params import Body

from adapters.api.auth.schema import LoginCredentialsSchema
from aioinject import Injected
from aioinject.ext.fastapi import inject
from result import Err


class AuthController(Controller):
    path = ""
    tags = ("Auth endpoints",)

    @post("/auth/login", status_code=200)
    @inject
    async def login(
        self,
        service: Injected[AuthenticationService],
        data: Annotated[LoginCredentialsSchema, Body()],
    ) -> dict[str, str]:
        dto = LoginCredentialsDTO(
            service_name=data.login, password=data.password
        )
        result = await service.login(dto)
        if isinstance(result, Err):
            match result.err_value:
                case ObjectNotFoundError() | BadPasswordError():
                    raise UnauthorizedHTTPError()
                case TokenEncodeError():
                    raise TokenCreateHTTPError()
                case _ as never:
                    assert_never(never)

        token = result.ok_value
        return {"token": token}
