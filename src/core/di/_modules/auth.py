import aioinject

from collections.abc import Iterable
from typing import Any

from core.domain.auth.repository import AuthRepository
from core.domain.auth.service import AuthService

Providers: type = Iterable[aioinject.Provider[Any]]

PROVIDERS: Providers = [
    aioinject.Scoped(AuthService),
    aioinject.Scoped(AuthRepository),
]
