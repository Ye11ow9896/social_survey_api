from typing import TypeVar, Any

from database.models.base import Base

_TModel = TypeVar("_TModel", bound=Base)


def get_value_or_empty(model: type[_TModel] | None, item: str) -> Any:
    if model is not None:
        return model.__getattribute__(item)
    return "Отсутствует"
