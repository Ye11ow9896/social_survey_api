from typing import Protocol, Any
from litestar import Request, Response
from adapters.api.schema import APIDetailSchema
from http import HTTPStatus


class BaseHTTPErrorProtocol(Protocol):
    status_code: int
    detail_schema: APIDetailSchema
    code: str


class BaseHTTPError(BaseHTTPErrorProtocol, Exception):
    pass


def app_exception_handler(
    request: Request[Any, Any, Any], exc: BaseHTTPError
) -> Response[Any]:
    return Response(
        content={"path": request.url.path, "detail": exc.detail_schema},
        status_code=exc.status_code,
    )


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
