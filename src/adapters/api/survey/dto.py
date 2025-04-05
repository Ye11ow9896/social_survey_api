from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class SurveyCreateDTO:
    name: str
    description: str | None