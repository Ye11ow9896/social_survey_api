from sqladmin import ModelView

from src.adapters.admin.utils import get_value_or_empty
from src.database.models import TelegramUser


class TelegramUserView(ModelView, model=TelegramUser):
    column_list = [
        TelegramUser.id,
        TelegramUser.role_id,
        TelegramUser.role,
    ]
    column_formatters = {
        TelegramUser.role: lambda m, a: get_value_or_empty(m.role, "name"),  # type: ignore[attr-defined]
    }
