class ObjectNotFoundError(Exception):
    def __init__(self, obj: str, field: str | None = None) -> None:
        self.message = f"Объект `{obj}` не найден"
        if field:
            self.message += f" со значением `{field}`"


class ObjectAlreadyExistsError(Exception):
    def __init__(self, obj: str, field: str | None = None) -> None:
        self.message = f"Объект `{obj}` уже существует"
        if field:
            self.message += f" со значением `{field}`"
