from typing import Annotated

from src.core.dto import BaseDataclass, snake_to_camel
from litestar.dto import DataclassDTO

class AuthDataclass(BaseDataclass):
    username: str
    password: str

AuthDTO = DataclassDTO[Annotated[AuthDataclass, snake_to_camel]]