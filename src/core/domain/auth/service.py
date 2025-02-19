import hashlib
from datetime import timedelta

from adapters.api.auth.dto import LoginCredentialsDTO
from core.domain.auth.exceptions import BadPasswordError, TokenEncodeError
from core.domain.auth.jwt import JWTAuthenticator
from core.domain.auth.repository import AuthRepository
from core.exceptions import ObjectNotFoundError
from database.models.auth_service import AuthService
from settings import AuthSettings
from result import Ok, Result, Err


class AuthenticationService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        jwt_authenticator: JWTAuthenticator,
        settings: AuthSettings,
    ) -> None:
        self._auth_repository = auth_repository
        self._jwt_authenticator = jwt_authenticator
        self._settings = settings

    async def login(
        self, dto: LoginCredentialsDTO
    ) -> Result[
        str,
        ObjectNotFoundError | BadPasswordError | TokenEncodeError,
    ]:
        service = await self._auth_repository.get_service(dto.service_name)
        if service is None:
            return Err(
                ObjectNotFoundError(obj=AuthService.__name__, field="name")
            )

        verify = self._verify_password(
            password=dto.password, hash_password=service.hash_password
        )
        if isinstance(verify, Err):
            return verify

        if token := self._jwt_authenticator.create_token(
            timedelta(minutes=15), service.service_name
        ):
            return Ok(token)

        return Err(TokenEncodeError())

    def _verify_password(
        self,
        password: str,
        hash_password: str,
    ) -> Result[None, BadPasswordError]:
        hashed_password = self._get_hashed_password(password=password)
        if hashed_password == hash_password:
            return Ok(None)

        return Err(BadPasswordError())

    def _get_hashed_password(self, password: str) -> str:
        convert_password = str.encode(
            password + self._settings.salt, encoding="utf-8"
        )
        return hashlib.md5(convert_password).hexdigest()

