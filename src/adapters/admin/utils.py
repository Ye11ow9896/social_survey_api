from typing import TypeVar

from database.models.base import Base

_TModel = TypeVar("_TModel", bound=Base)

def get_value_or_empty(model: type[_TModel], item: str):
    if model is not None:
        return model.__getattribute__(item)
    return "Отсутствует"
