from sqladmin import ModelView

from src.database.models.questionnaire import Questionnaire, QuestionnaireQuestion

class QuestionnaireView(ModelView, model=Questionnaire):
    column_list = [
        Questionnaire.id,
        Questionnaire.name,
        Questionnaire.survey_id,
    ]

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
