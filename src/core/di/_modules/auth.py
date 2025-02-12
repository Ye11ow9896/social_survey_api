import aioinject

from collections.abc import Iterable
from typing import Any, TypeAlias

from core.domain.auth.repository import AuthRepository
from core.domain.auth.service import AuthService

Providers: TypeAlias = Iterable[aioinject.Provider[Any]]

PROVIDERS: Providers = [
    aioinject.Scoped(AuthService),
    aioinject.Scoped(AuthRepository),
]