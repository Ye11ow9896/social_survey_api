from adapters.api.auth.controller import AuthController
from litestar.types import ControllerRouterHandler
from adapters.api.common.controller import CommonController
from adapters.api.telegram_user.controller import TelegramUserController

route_handlers: list[ControllerRouterHandler] = [
    CommonController,
    AuthController,
    TelegramUserController,
]
