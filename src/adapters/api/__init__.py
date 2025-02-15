from adapters.api.auth.controller import AuthController
from litestar.types import ControllerRouterHandler


route_handlers: list[ControllerRouterHandler] = [
    AuthController,
]
