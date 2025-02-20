class TokenDecodeError(Exception): ...


class TokenEncodeError(Exception): ...


class BadPasswordError(Exception): ...


class TokenNotFoundInHeaders(Exception): ...


class UnauthorizedError(Exception):
    def __init__(self, message: str | None) -> None:
        self.message = message


class TokenExpiredError(Exception):
    def __init__(self) -> None:
        self.message = "Срок токена истек"
