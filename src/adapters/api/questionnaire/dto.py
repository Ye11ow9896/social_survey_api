from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AssignQuestionnaireDTO:
    tg_id: int | None = None
    is_active: bool | None = None
    questionnaire_id: UUID | None = None
