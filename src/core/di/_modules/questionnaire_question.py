import aioinject

from src.core.domain.questionnaire.repository import (
    QuestionnaireQuestionRepository,
)
from src.core.di.di import Providers


PROVIDERS: Providers = [
    aioinject.Scoped(QuestionnaireQuestionRepository),
]
