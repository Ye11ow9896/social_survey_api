from sqladmin import ModelView

from src.database.models.survey import Survey


class SurveyView(ModelView, model=Survey):
    column_list = [
        Survey.id,
        Survey.name,
        Survey.description,
        Survey.created_at,
        Survey.updated_at,
    ]

