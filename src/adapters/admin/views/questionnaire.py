from sqladmin import ModelView

from src.adapters.admin.utils import get_value_or_empty
from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)


class QuestionnaireView(ModelView, model=Questionnaire):
    column_list = [
        Questionnaire.id,
        Questionnaire.name,
        Questionnaire.survey,
    ]
    column_formatters = {
        Questionnaire.survey: lambda m, a: get_value_or_empty(
            m.survey,  # type: ignore[attr-defined]
            "name",
        ),
    }


class QuestionnaireQuestionView(ModelView, model=QuestionnaireQuestion):
    column_list = [
        QuestionnaireQuestion.id,
        QuestionnaireQuestion.question_text,
        QuestionnaireQuestion.number,
        QuestionnaireQuestion.choice_text,
        QuestionnaireQuestion.written_text,
        QuestionnaireQuestion.question_type,
        QuestionnaireQuestion.questionnaire,
    ]
    column_formatters = {
        QuestionnaireQuestion.questionnaire: lambda m, a: get_value_or_empty(
            model=m.questionnaire,  # type: ignore[attr-defined]
            item="name",
        ),
    }
