class ObjectNotFoundError(Exception):
    def __init__(self, obj: str, field: str | None = None) -> None:
        self._msg = f"Объект `{obj}` не найден"
        if field:
            self._msg += f" со значением `{field}`"
