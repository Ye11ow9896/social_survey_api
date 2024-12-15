from litestar import Litestar

from src.adapters.api import route_handlers


def create_app() -> Litestar:

    return Litestar(
        route_handlers=route_handlers,
    )
