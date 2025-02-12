from lib.base_model import AppBaseModel
from pydantic import ConfigDict


class BaseDTO(AppBaseModel):
    model_config = ConfigDict(from_attributes=True)
