from datetime import datetime, timedelta
from typing import Any

from pydantic_core._pydantic_core import ValidationError

from core.domain.auth.dto import TokenPayloadDTO
from jose import jwt, JOSEError

from lib.contexmanagers import Suppress
from result import Ok, Result, Err
from lib.utils import utc_now
from settings import AuthSettings


class TokenExpiredError:
    pass


class JWTAuthenticator:
    def __init__(
        self,
        settings: AuthSettings,
    ) -> None:
        self._settings = settings

    def check_token_expired(
        self,
        payload_dto: TokenPayloadDTO,
        expire_delta: timedelta,
    ) -> Result[None, TokenExpiredError]:
        token_expire = (
            datetime.fromisoformat(payload_dto.expire) + expire_delta
        )
        if token_expire <= utc_now():
            return Err(TokenExpiredError())
        return Ok(None)

    def create_token(
        self, expires_delta: timedelta, service_name: str
    ) -> str | None:
        expire = utc_now() + expires_delta
        payload_dto = TokenPayloadDTO(
            service_name=service_name,
            expire=expire.isoformat(),
        )
        return self._encode(payload_dto)

    def _encode(self, payload_dto: TokenPayloadDTO) -> str | None:
        access_token = None
        with Suppress(ValidationError, JOSEError):
            access_token: str = jwt.encode(
                payload_dto.dict(),
                self._settings.secret,
                self._settings.jwt_crypt_algorythm,
            )

        return access_token

    def _decode(self, token: str) -> TokenPayloadDTO | None:
        payload_dto = None
        with Suppress(ValidationError, JOSEError):
            payload: dict[str, Any] = jwt.decode(
                token,
                self._settings.secret,
                self._settings.jwt_crypt_algorythm,
            )
            payload_dto = TokenPayloadDTO(
                service_name=payload.get("service_name"),
                expire=payload.get("expire"),
            )

        return payload_dto
