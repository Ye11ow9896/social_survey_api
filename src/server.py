from contextlib import asynccontextmanager, aclosing
from pathlib import Path

from src.adapters.api.questionnaire.controller import QuestionnaireController
from src.adapters.api.auth.controller import AuthController
from src.adapters.api.common.controller import CommonController
from src.adapters.api.telegram_user.controller import TelegramUserController
from src.adapters.api.survey.controller import SurveyController
from src.adapters.api.exceptions import BaseHTTPError
from src.adapters.api.handlers import app_exception_handler
from litestar import Litestar
from litestar.logging import LoggingConfig
from litestar.types import ControllerRouterHandler


from src.adapters.admin.admin import get_admin_plugin
from src.core.di import create_container
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec.components import Components
from litestar.openapi.spec.security_scheme import SecurityScheme
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine

from aioinject.ext.litestar import AioInjectPlugin

route_handlers: list[ControllerRouterHandler] = [
    CommonController,
    AuthController,
    TelegramUserController,
    SurveyController,
    QuestionnaireController,
]


@asynccontextmanager
async def lifespan(app: Litestar):  # type: ignore[no-untyped-def]
    async with aclosing(create_container()):
        yield


def create_app() -> Litestar:
    openapi_config = OpenAPIConfig(
        title="My API",
        version="1.0.0",
        security=[{"BearerToken": []}],
        components=Components(
            security_schemes={
                "BearerToken": SecurityScheme(type="http", scheme="bearer")
            }
        ),
    )
    return Litestar(
        route_handlers=route_handlers,
        lifespan=[lifespan],
        plugins=[AioInjectPlugin(create_container()), get_admin_plugin()],
        exception_handlers={BaseHTTPError: app_exception_handler},
        openapi_config=openapi_config,
        template_config=TemplateConfig(
            directory=Path(__file__).parent.parent / "static",
            engine=JinjaTemplateEngine,
        ),
        logging_config=LoggingConfig(
            root={"level": "INFO", "handlers": ["queue_listener"]},
            formatters={
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            log_exceptions="always",
        ),
    )
