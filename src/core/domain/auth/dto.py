from typing import Annotated
from pydantic import BeforeValidator
from src.core.dto import BaseDTO


class TokenPayloadDTO(BaseDTO):
    service_name: str
    expire: Annotated[str, BeforeValidator(lambda value: str(value))]
