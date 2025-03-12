from sqladmin import ModelView

from src.database.models import Survey


class SurveyView(ModelView, model=Survey):
    column_list = [
        Survey.id,
        Survey.created_at,
        Survey.name,
    ]
