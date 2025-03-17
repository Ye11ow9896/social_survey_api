from http import HTTPStatus

from src.adapters.api.exceptions import BaseHTTPError
from src.adapters.api.schema import APIDetailSchema


class QuestionnaireCreateUpdateHTTPError(BaseHTTPError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "questionnaire_create_update_error"

    def __init__(self, message: str) -> None:
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code,
            code=self.code,
            message=message,
        )
