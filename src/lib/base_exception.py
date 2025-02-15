class AppBaseException(Exception):
    def __init__(
        self,
        code: int | None = None,
        message: str | None = None,
    ) -> None:
        self.code = code
        self.message = message
