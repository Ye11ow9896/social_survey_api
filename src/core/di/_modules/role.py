import aioinject

from core.di.di import Providers
from core.domain.role.repository import RoleRepository


PROVIDERS: Providers = [
    aioinject.Scoped(RoleRepository),
]
