from datetime import datetime
from uuid import UUID

from database.enums import SexEnum
from lib.base_model import AppBaseModel


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
