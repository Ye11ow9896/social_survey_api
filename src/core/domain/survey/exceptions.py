from src.database.enums import RoleCodeEnum


class PermissionDeniedForRoleError(Exception):
    def __init__(self, current_role: RoleCodeEnum) -> None:
        self.message = (
            f"Доступ пользователя с ролью {current_role.value} запрещен"
        )
