import aioinject

from src.core.di.di import Providers
from src.core.domain.auth.jwt import JWTAuthenticator
from src.core.domain.auth.repository import AuthRepository
from src.core.domain.auth.service import AuthenticationService

PROVIDERS: Providers = [
    aioinject.Scoped(JWTAuthenticator),
    aioinject.Scoped(AuthRepository),
    aioinject.Scoped(AuthenticationService),
]
