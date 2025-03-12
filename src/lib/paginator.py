from dataclasses import dataclass
from typing import TypeVar, Generic, Sequence, Self

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dto import BaseDTO

from src.lib.base_model import AppBaseModel

_T = TypeVar("_T")
_T_Model = TypeVar("_T_Model", bound=AppBaseModel)


class PaginationDTO(BaseDTO):
    page: int
    page_size: int


@dataclass(frozen=True, slots=True)
class PaginationResultDTO(Generic[_T_Model]):
    items: Sequence[_T_Model]
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
        dto_model: _T_Model,
        pagination: PaginationDTO,
    ) -> PaginationResultDTO[_T_Model]:
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
            items=dto_model.sqlalchemy_model_validate_list(items),
            has_next_page=pagination.page * pagination.page_size < count,
            count=count,
        )
