from collections.abc import Iterable
from typing import Any, Self

from pydantic import BaseModel


class AppBaseModel(BaseModel):
    @classmethod
    def model_validate_optional(cls, model: object | None) -> Self | None:
        if model is None:
            return None
        return cls.model_validate(model)

    @classmethod
    def model_validate_list(cls, models: Iterable[Any]) -> list[Self]:
        return [cls.model_validate(model) for model in models]
