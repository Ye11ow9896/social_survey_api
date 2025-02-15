from typing import assert_never

from adapters.api.auth.exceptions import (
    UnauthorizedHTTPError,
    TokenCreateHTTPError,
)
from core.domain.auth.dto import LoginCredentialsDTO
from core.domain.auth.exceptions import BadPasswordError, TokenEncodeError
from core.domain.auth.service import AuthenticationService
from core.exceptions import ObjectNotFoundError

from litestar import get
from litestar.controller import Controller

from adapters.api.auth.schema import LoginCredentialsSchema
from aioinject import Injected
from aioinject.ext.fastapi import inject
from result import Err


class AuthController(Controller):
    path = ""
    tags = ("Auth endpoints",)

    @get("/authorization", status_code=200)
    @inject
    async def test(
        self,
            id: int,
        service: Injected[AuthenticationService],

        #schema: LoginCredentialsSchema,
    ) -> dict[str, str]:
        dto = LoginCredentialsDTO(
            service_name="schema.login", password="schema.password"
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
