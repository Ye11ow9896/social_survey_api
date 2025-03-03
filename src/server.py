from contextlib import asynccontextmanager, aclosing


from adapters.api.exceptions import app_exception_handler, BaseHTTPError
from litestar import Litestar

from admin.admin import get_admin_plugin
from core.di import create_container
from litestar.middleware.base import DefineMiddleware
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec.components import Components
from litestar.openapi.spec.security_scheme import SecurityScheme
from core.domain.auth.middleware import CheckAccessTokenMiddleware
from database.engine import engine
from database.models import TelegramUser
from src.adapters.api import route_handlers
from aioinject.ext.litestar import AioInjectPlugin
from sqladmin_litestar_plugin import SQLAdminPlugin
from sqladmin import ModelView


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
        plugins=[
            AioInjectPlugin(create_container()),
            get_admin_plugin()
        ],
        exception_handlers={BaseHTTPError: app_exception_handler},
        openapi_config=openapi_config,
    )
