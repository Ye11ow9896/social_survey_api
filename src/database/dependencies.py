import contextlib
from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from .engine import async_session_factory

@contextlib.asynccontextmanager
async def create_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session

