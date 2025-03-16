from src.adapters.api.schema import BaseSchema
from src.adapters.api.survey.dto import SurveyCreateDTO

class SurveyCreateSchema(BaseSchema):
    name: str
    description: str | None

    def to_dto(self) -> SurveyCreateDTO:
        return SurveyCreateDTO(
            name=self.name,
            description=self.description,
        )