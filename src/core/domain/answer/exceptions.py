from uuid import UUID


class WrittenAnswerCreateTypeError(Exception):
    def __init__(self, question_id: UUID, current_type: str) -> None:
        self.message = f"Ошибка создания ответа. У вопроса `{question_id}` тип `{current_type}`. Должен быть written"
