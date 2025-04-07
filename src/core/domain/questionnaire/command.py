from jinja2 import Environment, FileSystemLoader, select_autoescape
from uuid import UUID

from src.core.domain.questionnaire.service import QuestionnaireService

# вынести в отдельный файл?
# loader - откуда загружаем шаблон
env = Environment(
    loader=FileSystemLoader('template'),
    autoescape=select_autoescape(['html', 'xml'])
)

# это шаблон страницы
template = env.get_template('template.html')

class GetQuestionnaireFormCommand:
    def __init__(
            self,
            questionnaire_servive: QuestionnaireService,
    ) -> None:
        self._questionnaire_servive = questionnaire_servive

    async def get_questionnaire_form(
            self, 
            questionnaire_id: UUID
        ):
        # questionnaire = self._questionnaire_servive.get_questionnaire_by_id(questionnaire_id)

        # Пока тестовые данные
        questions = {
    1: {
        "name": "name",
        "label": "Ваше имя:",
        "question_type": "WRITTEN"
    },
        }   

        rendered_page = template.render()

        return rendered_page



