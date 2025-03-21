from http import HTTPStatus

from ..exceptions import BaseHTTPError
from ..schema import APIDetailSchema


class UnauthorizedHTTPError(BaseHTTPError):
    status_code = HTTPStatus.UNAUTHORIZED
    code = "bad_login_or_password"

    def __init__(
        self,
    ) -> None:
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code,
            code=self.code,
            message="Ошибка авторизации. Неверный логин или пароль",
        )


class TokenCreateHTTPError(BaseHTTPError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    code = "token_create_error"

    def __init__(
        self,
    ) -> None:
        self.error_schema = APIDetailSchema(
            status_code=self.status_code,
            code=self.code,
            message="Возникла ошибка при создании токена. Обратитесь в поддержку",
        )
