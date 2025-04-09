from jinja2 import Environment, FileSystemLoader, select_autoescape
from uuid import UUID

from result import Err, Ok, Result

from src.database.models.questionnaire import Questionnaire
from src.core.exceptions import ObjectNotFoundError
from src.core.domain.questionnaire.service import QuestionnaireService

# вынести в отдельный файл?
# loader - откуда загружаем шаблон
env = Environment(
    loader=FileSystemLoader("static"),
    autoescape=select_autoescape(["html", "xml"]),
)

# это шаблон страницы
template = env.get_template("template.html")


class GetQuestionnaireFormCommand:
    def __init__(
        self,
        questionnaire_servive: QuestionnaireService,
    ) -> None:
        self._questionnaire_servive = questionnaire_servive

    async def get_questionnaire_form(
        self,
        questionnaire_id: UUID,
    ) -> Result[str, ObjectNotFoundError]:
        questionnaire = (
            await self._questionnaire_servive.get_questionnaire_by_id(
                questionnaire_id
            )
        )
        if questionnaire is None:
            return Err(ObjectNotFoundError(obj=Questionnaire.__name__))
        return Ok(
            template.render(
                questionnaire=questionnaire.ok_value,
                questions=questionnaire.ok_value.questionnaire_questions,
            )
        )
