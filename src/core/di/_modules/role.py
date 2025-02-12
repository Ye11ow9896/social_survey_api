import aioinject

from collections.abc import Iterable
from typing import Any, TypeAlias

from core.domain.role.repository import RoleRepository

Providers: TypeAlias = Iterable[aioinject.Provider[Any]]

PROVIDERS: Providers = [
    aioinject.Scoped(RoleRepository),
]



