from typing import Any

from litestar import Request, Response

from src.adapters.api.exceptions import BaseHTTPError


def app_exception_handler(
    request: Request[Any, Any, Any], exc: BaseHTTPError
) -> Response[Any]:
    return Response(
        content={"path": request.url.path, "detail": exc.detail_schema},
        status_code=exc.status_code,
    )
