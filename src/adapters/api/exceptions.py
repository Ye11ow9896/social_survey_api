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
