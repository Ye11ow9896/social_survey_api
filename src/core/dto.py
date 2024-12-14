from dataclasses import dataclass

from litestar.dto import DTOConfig

snake_to_camel = DTOConfig(rename_strategy="camel")


@dataclass(slots=True, frozen=True)
class BaseFrozenDataclass:
    ...


@dataclass(slots=True)
class BaseDataclass:
    ...

