from adapters.api.auth.exceptions import UnauthorizedBadTokenHTTPError
from core.di import create_container
from core.domain.auth.exceptions import (
    TokenNotFoundInHeaders,
    TokenExpiredError,
    TokenDecodeError,
)
from core.domain.auth.jwt import JWTAuthenticator
from litestar.connection import ASGIConnection
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from result import Ok, Result, Err


class CheckAccessTokenMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(
        self,
        connection: ASGIConnection,  # type: ignore[type-arg]
    ) -> AuthenticationResult:
        token = connection.headers.get("authorization")
        result = await self._check_token(token)
        if isinstance(result, Err):
            raise UnauthorizedBadTokenHTTPError(
                "Ошибка доступа. Не авторизован"
            )
        return AuthenticationResult(user="user", auth=token)

    async def _check_token(
        self, token: str | None
    ) -> Result[
        None, TokenNotFoundInHeaders | TokenExpiredError | TokenDecodeError
    ]:
        if not token:
            return Err(TokenNotFoundInHeaders())
        container = create_container()
        async with container.context() as ctx:
            jwt_authenticator = await ctx.resolve(JWTAuthenticator)
            result = jwt_authenticator.check_token_expired(token)
        if isinstance(result, Err):
            return result
        return Ok(None)
