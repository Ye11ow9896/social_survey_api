from sqladmin import ModelView

from src.database.models.questionnaire import (
    Questionnaire,
    QuestionnaireQuestion,
)


class QuestionnaireView(ModelView, model=Questionnaire):
    form_columns = [
        Questionnaire.name,
        Questionnaire.survey_id,  
    ]
    column_list = [
        Questionnaire.id,
        Questionnaire.name,
        Questionnaire.survey_id,
        Questionnaire.questionnaire_questions,
    ]
    column_formatters = {
        Questionnaire.questionnaire_questions: lambda m, a: ", ".join(q.question_text for q in m.questionnaire_questions)
        }
    # form_ajax_refs = {
    # "survey_id": {
    #     "fields": ("name", "description"),  # Поля Survey для поиска
    #     "order_by": "name",  # Сортировка
    # }
    # }


class QuestionnaireQuestionView(ModelView, model=QuestionnaireQuestion):
    column_list = [
        QuestionnaireQuestion.id,
        QuestionnaireQuestion.questionnaire_id,
        QuestionnaireQuestion.question_text,
        QuestionnaireQuestion.number,
        QuestionnaireQuestion.choice_text,
        QuestionnaireQuestion.written_text,
        QuestionnaireQuestion.question_type,
    ]
