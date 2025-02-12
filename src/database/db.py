from collections.abc import Iterable, Sequence
from typing import Protocol, TypeVar

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy.sql.selectable import ForUpdateParameter

from database.models.base import Base

T = TypeVar("T", bound=DeclarativeBase)


class DBContext(Protocol):

    def add(self, model: T) -> None: ...

    def add_all(self, models: Iterable[Base]) -> None: ...

    async def flush(self, objects: Sequence[T] | None = ...) -> None: ...

    async def merge(
        self,
        instance: T,
        *,
        load: bool = True,
        options: Sequence[ORMOption] | None = None,
    ) -> T: ...

    async def refresh(
        self,
        instance: object,
        attribute_names: Iterable[str] | None = None,
        with_for_update: ForUpdateParameter = None,
    ) -> None: ...
