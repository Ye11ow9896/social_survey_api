from typing import Protocol, Any
from litestar import Request, Response
from adapters.api.schema import APIErrorSchema
from http import HTTPStatus


class BaseHTTPErrorProtocol(Protocol):
    status_code: int
    error_schema: APIErrorSchema
    code: str


class BaseHTTPError(BaseHTTPErrorProtocol, Exception):
    pass


def app_exception_handler(
    request: Request[Any, Any, Any], exc: BaseHTTPError
) -> Response[Any]:
    return Response(
        content={"path": request.url.path, "error_detail": exc.error_schema},
        status_code=exc.status_code,
    )


class ObjectNotFoundHTTPError(BaseHTTPError):
    status_code = HTTPStatus.NOT_FOUND
    code = "object_not_found"

    def __init__(
        self,
        message: str,
    ):
        self.error_schema = APIErrorSchema(code=self.code, message=message)
