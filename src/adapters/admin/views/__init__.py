from src.adapters.admin.views.role import RoleView
from src.adapters.admin.views.survey import SurveyView
from src.adapters.admin.views.telegram_user import TelegramUserView
from src.adapters.admin.views.questionnaire import (
    QuestionnaireView,
    QuestionnaireQuestionView,
)


_VIEWS = [
    TelegramUserView,
    RoleView,
    SurveyView,
    QuestionnaireView,
    QuestionnaireQuestionView,
]
