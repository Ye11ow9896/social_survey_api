from datetime import datetime
from typing import Annotated
from uuid import UUID

from src.database.models.role import Role
from src.database.models import TelegramUser
from src.database.enums import RoleCodeEnum, SexEnum
from src.lib.base_model import AppBaseModel
from sqla_filter import UNSET, BaseFilter, FilterField, Unset
from sqlalchemy.sql.operators import eq


class TelegramUserDTO(AppBaseModel):
    role_id: UUID
    age: int | None
    sex: SexEnum | None
    real_first_name: str | None
    real_middle_name: str | None
    real_last_name: str | None
    updated_at: datetime
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    url: str
    is_bot: bool
    is_premium: bool


class TelegramUserFilterDTO(BaseFilter):
    tg_id: Annotated[
        int | Unset,
        FilterField(TelegramUser.tg_id, operator=eq),
    ] = UNSET
    is_bot: Annotated[
        bool | Unset,
        FilterField(TelegramUser.is_bot, operator=eq),
    ] = UNSET
    id: Annotated[
        UUID | Unset,
        FilterField(TelegramUser.id, operator=eq),
    ] = UNSET
    role: Annotated[
        RoleCodeEnum | Unset,
        FilterField(Role.code, operator=eq),
    ] = UNSET
