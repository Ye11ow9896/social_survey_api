from typing import Protocol
from src.adapters.api.schema import APIDetailSchema
from http import HTTPStatus


class BaseHTTPErrorProtocol(Protocol):
    status_code: int
    detail_schema: APIDetailSchema
    code: str


class BaseHTTPError(BaseHTTPErrorProtocol, Exception):
    pass


class ObjectNotFoundHTTPError(BaseHTTPError):
    status_code = HTTPStatus.NOT_FOUND
    code = "object_not_found"

    def __init__(
        self,
        message: str,
    ):
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code, code=self.code, message=message
        )


class ObjectAlreadyExistsHTTPError(BaseHTTPError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "object_already_exists"

    def __init__(
        self,
        message: str,
    ):
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code, code=self.code, message=message
        )


class PermissionDeniedForRoleHTTPError(BaseHTTPError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "permission_denied_error"

    def __init__(self, message: str) -> None:
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code,
            code=self.code,
            message=message,
        )
