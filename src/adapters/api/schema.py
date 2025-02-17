from lib.base_model import AppBaseModel

from pydantic import ConfigDict

from lib.utils import _snake_to_camel


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
