from decimal import Decimal
from typing import Annotated
from collections.abc import Mapping
from uuid import UUID

from sqlalchemy import Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

numeric_10_2 = Annotated[
    Decimal, mapped_column(Numeric(precision=10, scale=2))
]
str_16 = Annotated[str, 16]


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)


def create_comment(comment: str) -> Mapping[str, str]:
    return {"comment": comment}
