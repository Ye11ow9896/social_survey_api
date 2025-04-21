class PermissionDeniedForRoleError(Exception):
    def __init__(self, current_role: str) -> None:
        self.message = f"Доступ пользователя с ролью {current_role} запрещен."