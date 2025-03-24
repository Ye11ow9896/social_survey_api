from src.adapters.api.schema import BaseSchema
from src.adapters.api.telegram_user.dto import TelegramUserCreateDTO
from src.database.enums import RoleCodeEnum


class TelegramUserCreateSchema(BaseSchema):
    age: int | None
    sex: int | None
    real_first_name: str | None
    real_middle_name: str | None
    real_last_name: str | None
    tg_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    url: str
    is_bot: bool
    is_premium: bool | None

    def to_dto(self, role: RoleCodeEnum) -> TelegramUserCreateDTO:
        role_id = role.identifier
        return TelegramUserCreateDTO(
            role_id=role_id,
            url=self.url,
            is_bot=self.is_bot,
            is_premium=self.is_premium,
            age=self.age,
            sex=self.sex,
            real_first_name=self.real_first_name,
            real_middle_name=self.real_middle_name,
            real_last_name=self.real_last_name,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class TelegramUserRoleSchema(BaseSchema):
    name: str
    code: RoleCodeEnum
