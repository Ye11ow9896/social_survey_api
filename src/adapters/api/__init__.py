from litestar.types import ControllerRouterHandler

from adapters.api.auth.controller import AuthController

route_handlers: list[ControllerRouterHandler] = [
    AuthController,
]
