from litestar.types import ControllerRouterHandler
from src.adapters.api.auth.controller import AuthController
from src.adapters.api.common.controller import CommonController
from src.adapters.api.survey.controller import SurveyController
from src.adapters.api.telegram_user.controller import TelegramUserController

route_handlers: list[ControllerRouterHandler] = [
    CommonController,
    AuthController,
    TelegramUserController,
    SurveyController,
]