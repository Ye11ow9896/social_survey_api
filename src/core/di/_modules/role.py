import aioinject

from collections.abc import Iterable
from typing import Any

from core.domain.role.repository import RoleRepository

Providers: type = Iterable[aioinject.Provider[Any]]

PROVIDERS: Providers = [
    aioinject.Scoped(RoleRepository),
]
