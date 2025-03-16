from contextlib import asynccontextmanager, aclosing
import logging
from litestar.logging import LoggingConfig


from src.adapters.api.exceptions import app_exception_handler, BaseHTTPError
from litestar import Litestar

from src.admin.admin import get_admin_plugin
from src.core.di import create_container
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec.components import Components
from litestar.openapi.spec.security_scheme import SecurityScheme

from src.adapters.api import route_handlers
from aioinject.ext.litestar import AioInjectPlugin


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
        logging_config=LoggingConfig(
        root={"level": "INFO", "handlers": ["queue_listener"]},
        formatters={
            "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        log_exceptions="always",
))
