from typing import assert_never, Annotated

from src.adapters.api.auth.dto import LoginCredentialsDTO
from src.adapters.api.auth.exceptions import (
    UnauthorizedBadCredentialsHTTPError,
    TokenCreateHTTPError,
)
from src.core.domain.auth.exceptions import BadPasswordError, TokenEncodeError
from src.core.domain.auth.service import AuthenticationService
from src.core.exceptions import ObjectNotFoundError

from litestar import post
from litestar.controller import Controller
from litestar.params import Body

from src.adapters.api.auth.schema import LoginCredentialsSchema
from aioinject import Injected
from aioinject.ext.litestar import inject
from result import Err


class AuthController(Controller):
    path = ""
    tags = ("Auth endpoints",)

    @post("/auth/login", status_code=200, exclude_from_auth=True)
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
                    raise UnauthorizedBadCredentialsHTTPError()
                case TokenEncodeError():
                    raise TokenCreateHTTPError()
                case _ as never:
                    assert_never(never)

        token = result.ok_value
        return {"token": token}
