from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SurveyCreateDTO:
    name: str
    description: str | None


@dataclass(slots=True, frozen=True)
class SurveyUpdateDTO:
    name: str | None = None
    description: str | None = None
