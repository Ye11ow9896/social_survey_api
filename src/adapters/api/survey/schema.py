from src.adapters.api.schema import BaseSchema
from src.adapters.api.survey.dto import SurveyCreateDTO


class SurveyCreateSchema(BaseSchema):
    tg_id: int
    name: str
    description: str | None

    def to_dto(self) -> SurveyCreateDTO:
        return SurveyCreateDTO(
            tg_id=self.tg_id,
            name=self.name,
            description=self.description,
        )
