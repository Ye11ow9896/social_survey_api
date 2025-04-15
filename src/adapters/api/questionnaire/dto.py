from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssignQuestionnaireDTO:
    tg_id: int | None = None
    is_active: bool | None = None
