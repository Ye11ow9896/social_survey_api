import aioinject

from src.core.di.di import Providers
from src.core.domain.role.repository import RoleRepository


PROVIDERS: Providers = [
    aioinject.Scoped(RoleRepository),
]
