import aioinject

from src.core.domain.answer.service import AnswerService
from src.core.domain.answer.repository import WrittenAnswerRepository
from src.core.di.di import Providers


PROVIDERS: Providers = [
    aioinject.Scoped(WrittenAnswerRepository),
    aioinject.Scoped(AnswerService),
]
