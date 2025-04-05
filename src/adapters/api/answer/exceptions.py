from http import HTTPStatus

from src.adapters.api.schema import APIDetailSchema
from src.adapters.api.exceptions import BaseHTTPError


class WrittenAnswerCreateTypeHTTPError(BaseHTTPError):
    status_code = HTTPStatus.BAD_REQUEST
    code = "written_answer_create_type_error"

    def __init__(self, message: str) -> None:
        self.detail_schema = APIDetailSchema(
            status_code=self.status_code,
            code=self.code,
            message=message,
        )
