from decimal import Decimal
from typing import Annotated
from uuid import UUID

from sqlalchemy import Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

numeric_10_2 = Annotated[Decimal, mapped_column(Numeric(precision=10, scale=2))]
numeric_10_3 = Annotated[Decimal, mapped_column(Numeric(precision=10, scale=3))]
numeric_22_2 = Annotated[Decimal, mapped_column(Numeric(precision=22, scale=2))]
numeric_3_1 = Annotated[Decimal, mapped_column(Numeric(precision=3, scale=2))]

str_3 = Annotated[str, 3]
str_10 = Annotated[str, 10]
str_16 = Annotated[str, 16]
str_20 = Annotated[str, 20]
str_32 = Annotated[str, 32]
str_60 = Annotated[str, 60]
str_64 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_255 = Annotated[str, 255]
str_500 = Annotated[str, 500]
str_512 = Annotated[str, 512]

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)
