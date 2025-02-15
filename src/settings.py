import functools
from typing import TypeVar
from urllib.parse import quote_plus

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

_TSetting = TypeVar("_TSetting", bound=BaseSettings)


def get_settings(cls: type[_TSetting]) -> _TSetting:
    dotenv.load_dotenv()
    return cls()


get_settings = functools.lru_cache(get_settings)


class PostgresqlSettings(BaseSettings):
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, env_prefix="database_"
    )

    driver: str = "postgresql+asyncpg"
    name: str
    username: str
    password: str
    host: str
    echo: bool = False

    @property
    def url(self) -> str:
        password = quote_plus(self.password)
        return f"{self.driver}://{self.username}:{password}@{self.host}/{self.name}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, env_prefix="auth_"
    )

    secret: str
    jwt_crypt_algorythm: str
    access_token_expire: int
    salt: str
