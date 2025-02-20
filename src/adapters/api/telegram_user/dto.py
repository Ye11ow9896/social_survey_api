from dataclasses import dataclass
from typing import Annotated
from uuid import UUID
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq

from database.models import TelegramUser


@dataclass(slots=True, frozen=True)
class TelegramUserCreateDTO:
    role_id: UUID
    url: str
    is_bot: bool
    is_premium: bool
    age: int | None
    sex: int | None
    real_first_name: str | None
    real_middle_name: str | None
    real_last_name: str | None
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None


class TelegramUserFilterDTO(BaseFilter):
    tg_id: Annotated[
        UUID | Unset,
        FilterField(TelegramUser.tg_id, operator=eq),
    ] = UNSET
    is_bot: Annotated[
        str | Unset,
        FilterField(TelegramUser.is_bot, operator=eq),
    ] = UNSET