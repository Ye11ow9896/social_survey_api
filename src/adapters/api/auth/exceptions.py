from http import HTTPStatus

from ..exceptions import BaseHTTPError
from ..schema import APIDetailSchema


class UnauthorizedBadCredentialsHTTPError(BaseHTTPError):
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


class UnauthorizedBadTokenHTTPError(BaseHTTPError):
    status_code = HTTPStatus.UNAUTHORIZED
    code = "bad_token_authorization"

    def __init__(
        self,
        message: str
    ) -> None:
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code,
            code=self.code,
            message=message,
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
