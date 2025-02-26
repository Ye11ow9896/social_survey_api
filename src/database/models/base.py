from decimal import Decimal
from typing import Annotated
from collections.abc import Mapping
from uuid import UUID

from sqlalchemy import Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid_utils._uuid_utils import uuid7


numeric_10_2 = Annotated[
    Decimal, mapped_column(Numeric(precision=10, scale=2))
]
str_16 = Annotated[str, 16]

uuid_pk = Annotated[
    UUID,
    mapped_column(
        primary_key=True, default=uuid7, comment="Идентификатор записи"
    ),
]


class Base(DeclarativeBase):
    id: Mapped[uuid_pk] = mapped_column(primary_key=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def create_comment(comment: str) -> Mapping[str, str]:
    return {"comment": comment}
