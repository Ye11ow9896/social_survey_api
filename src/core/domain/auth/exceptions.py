class TokenDecodeError(Exception): ...


class TokenEncodeError(Exception): ...


class BadPasswordError(Exception): ...


class UnauthorizedError(Exception):
    def __init__(self, message: str | None) -> None:
        self.message = message
