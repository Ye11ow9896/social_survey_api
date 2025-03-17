from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class SurveyCreateDTO:
    name: str
    description: str | None


@dataclass(slots=True, frozen=True)
class SurveyUpdateDTO:
    name: str | None = None
    questionnaire_id: UUID | None = None
    description: str | None = None
