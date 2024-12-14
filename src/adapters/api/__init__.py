from src.adapters.api.auth import AuthController
from src.adapters.api.test import TestController
from litestar.types import ControllerRouterHandler


route_handlers: list[ControllerRouterHandler] = [
    TestController,
    AuthController,
]