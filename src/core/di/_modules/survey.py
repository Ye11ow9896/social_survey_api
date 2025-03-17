import aioinject

from src.core.di.di import Providers
from src.core.domain.survey.repository import SurveyRepository
from src.core.domain.survey.service import SurveyService

PROVIDERS: Providers = [
    aioinject.Scoped(SurveyService),
    aioinject.Scoped(SurveyRepository),
]
