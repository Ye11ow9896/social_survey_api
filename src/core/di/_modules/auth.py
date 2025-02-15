import aioinject

from core.di.di import Providers
from core.domain.auth.jwt import JWTAuthenticator
from core.domain.auth.repository import AuthRepository
from core.domain.auth.service import AuthenticationService

PROVIDERS: Providers = [
    aioinject.Scoped(JWTAuthenticator),
    aioinject.Scoped(AuthRepository),
    aioinject.Scoped(AuthenticationService),


]
