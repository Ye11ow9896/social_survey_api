class TelegramUserCreateError(Exception):
    def __init__(self, url: str) -> None:
        self.message = f"Ошибка создания пользователя {url} в системе"
