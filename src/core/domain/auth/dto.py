from typing import Annotated

from litestar.dto import DataclassDTO

from src.core.dto import BaseDataclass, snake_to_camel


class AuthDataclass(BaseDataclass):
    username: str
    password: str

AuthDTO = DataclassDTO[Annotated[AuthDataclass, snake_to_camel]]
