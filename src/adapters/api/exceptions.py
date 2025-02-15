from typing import Protocol

from adapters.api.schema import APIErrorSchema
from http import HTTPStatus


class BaseHTTPErrorProtocol(Protocol):
    status_code: int
    error_schema: APIErrorSchema
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
        self.error_schema = APIErrorSchema(code=self.code, message=message)
