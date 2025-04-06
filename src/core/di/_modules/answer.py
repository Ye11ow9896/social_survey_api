import aioinject

from src.core.domain.answer.service import AnswerService
from src.core.domain.answer.repository import QuestionAnswerRepository
from src.core.di.di import Providers


PROVIDERS: Providers = [
    aioinject.Scoped(QuestionAnswerRepository),
    aioinject.Scoped(AnswerService),
]
