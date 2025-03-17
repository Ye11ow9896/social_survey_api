from src.lib.base_model import AppBaseModel
from pydantic import ConfigDict


class BaseDTO(AppBaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseAssignDTO(AppBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        frozen=True,
    )
