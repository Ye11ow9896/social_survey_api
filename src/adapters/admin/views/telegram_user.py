from sqladmin import ModelView

from src.database.models import TelegramUser


class TelegramUserView(ModelView, model=TelegramUser):
    column_list = [
        TelegramUser.id,
        TelegramUser.role_id,
        TelegramUser.role,
        TelegramUser.surveys,
    ]
