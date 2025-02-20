from dataclasses import dataclass
from typing import TypeVar, Generic, Sequence, Self

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dto import BaseDTO

_T = TypeVar("_T")


class PaginationDTO(BaseDTO):
    page: int
    page_size: int


@dataclass(frozen=True, slots=True)
class PaginationResultDTO(Generic[_T]):
    items: Sequence[_T]
    has_next_page: bool
    count: int

    @classmethod
    def empty(cls) -> Self:
        return cls(items=[], has_next_page=False, count=0)


class PagePaginator:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def paginate(
        self,
        stmt: Select[tuple[_T]],
        *,
        pagination: PaginationDTO,
    ) -> PaginationResultDTO[_T]:
        paginated = stmt.offset(
            (pagination.page - 1) * pagination.page_size
        ).limit(
            pagination.page_size,
        )

        count = (
            await self._session.scalar(
                select(func.count()).select_from(stmt.subquery()),
            )
            or 0
        )
        items = (await self._session.scalars(paginated)).unique().all()
        return PaginationResultDTO(
            items=items,
            has_next_page=pagination.page * pagination.page_size < count,
            count=count,
        )
