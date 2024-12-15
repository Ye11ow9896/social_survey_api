from datetime import datetime, UTC, date


def utc_now() -> datetime:
    return datetime.now(tz=UTC)


def today() -> date:
    return utc_now().date()
