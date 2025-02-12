import aioinject

from collections.abc import Iterable
from typing import Any, TypeAlias

from core.domain.user.repository import UserRepository
from core.domain.user.service import UserService

Providers: TypeAlias = Iterable[aioinject.Provider[Any]]

PROVIDERS: Providers = [
    aioinject.Scoped(UserRepository),
    aioinject.Scoped(UserService),
]