from dataclasses import dataclass
from uuid import UUID


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
