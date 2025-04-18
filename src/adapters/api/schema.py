from typing import TypeVar, Generic

from src.lib.base_model import AppBaseModel

from pydantic import ConfigDict

from src.lib.utils import _snake_to_camel

_T = TypeVar("_T")


class BaseSchema(AppBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=_snake_to_camel,
    )


class APIDetailSchema(AppBaseModel):
    status_code: int
    code: str
    message: str


class PaginationResponseSchema(BaseSchema, Generic[_T]):
    count: int
    has_next_page: bool
    items: list[_T]
