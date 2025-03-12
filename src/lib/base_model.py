from collections.abc import Iterable
from typing import Any, Self, TypeVar

from pydantic import BaseModel

from src.database.models.base import Base

_T_Base = TypeVar("_T_Base", bound=Base)


class AppBaseModel(BaseModel):
    @classmethod
    def model_validate_optional(cls, model: object | None) -> Self | None:
        if model is None:
            return None
        return cls.model_validate(model)

    @classmethod
    def model_validate_list(cls, models: Iterable[Any]) -> list[Self]:
        return [cls.model_validate(model) for model in models]

    @classmethod
    def sqlalchemy_model_validate_optional(cls, model: _T_Base) -> Self | None:
        if model is None:
            return None
        return cls.model_validate(model.as_dict())

    @classmethod
    def sqlalchemy_model_validate_list(
        cls, models: Iterable[_T_Base]
    ) -> list[Self]:
        return [cls.model_validate(model.as_dict()) for model in models]
