from litestar.types import ControllerRouterHandler

from src.adapters.api.auth import AuthController
from src.adapters.api.test import TestController

route_handlers: list[ControllerRouterHandler] = [
    TestController,
    AuthController,
]