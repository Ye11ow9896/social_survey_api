from types import TracebackType
from typing import Self


class Suppress:
    def __init__(self, *exceptions: type[BaseException]) -> None:
        self._exceptions = exceptions

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        return exc_type is not None and issubclass(exc_type, self._exceptions)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        return exc_type is not None and issubclass(exc_type, self._exceptions)
