from contextlib import asynccontextmanager, aclosing

from litestar import Litestar

from core.di import create_container
from src.adapters.api import route_handlers
from aioinject.ext.litestar import AioInjectPlugin

@asynccontextmanager
async def lifespan(app: Litestar):
    async with aclosing(create_container()):
        yield

def create_app() -> Litestar:
    return Litestar(
        route_handlers=route_handlers,
        lifespan=[lifespan],
        plugins=[AioInjectPlugin(create_container())]
    )
