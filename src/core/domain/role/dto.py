from dataclasses import dataclass
from typing import Annotated

from database.enums import RoleCodeEnum
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from database.models import TelegramUser, Role


@dataclass(slots=True, frozen=True)
class RoleDTO:
    name: str
    code: RoleCodeEnum


class RoleFilterDTO(BaseFilter):
    tg_id: Annotated[
        int | Unset,
        FilterField(TelegramUser.tg_id, operator=eq),
    ] = UNSET
    name: Annotated[
        str | Unset,
        FilterField(Role.name, operator=eq),
    ] = UNSET
