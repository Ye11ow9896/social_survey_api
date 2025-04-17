import aioinject

from src.core.di.di import Providers
from src.core.domain.user.repository import (
    RespondentQuestionnaireRepository,
    TelegramUserRepository,
)
from src.core.domain.user.service import TelegramUserService

PROVIDERS: Providers = [
    aioinject.Scoped(TelegramUserService),
    aioinject.Scoped(TelegramUserRepository),
    aioinject.Scoped(RespondentQuestionnaireRepository),
]
