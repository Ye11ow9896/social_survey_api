from sqladmin import ModelView

from src.database.models import Role


class RoleView(ModelView, model=Role):
    column_list = [Role.id, Role.name]
