import aioinject

from core.di.di import Providers
from core.domain.user.repository import TelegramUserRepository
from core.domain.user.service import TelegramUserService

PROVIDERS: Providers = [
    aioinject.Scoped(TelegramUserService),
    aioinject.Scoped(TelegramUserRepository),
]
