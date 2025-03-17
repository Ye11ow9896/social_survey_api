import enum

class QuestionType(enum.StrEnum):
    WRITTEN = "written"
    MULTIPLE_CHOICE = "multiple_choice"
    ONE_CHOICE = "one_choice"