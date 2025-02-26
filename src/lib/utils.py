from datetime import datetime, UTC, date
from inspect import isclass


def _snake_to_camel(name: str) -> str:
    first, *rest = name.split("_")
    return first + "".join(map(str.capitalize, rest))


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def today() -> date:
    return utc_now().date()
