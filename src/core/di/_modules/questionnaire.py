import aioinject

from src.core.domain.questionnaire.repository import (
    QuestionnaireRepository,
    QuestionTextRepository,
    QuestionnaireQuestionRepository,
)
from src.core.domain.questionnaire.service import QuestionnaireService
from src.core.di.di import Providers


PROVIDERS: Providers = [
    aioinject.Scoped(QuestionnaireService),
    aioinject.Scoped(QuestionnaireRepository),
    aioinject.Scoped(QuestionnaireQuestionRepository),
    aioinject.Scoped(QuestionTextRepository),
]
