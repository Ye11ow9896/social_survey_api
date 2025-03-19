class QuestionnaireCreateUpdateQuestionError(Exception):
    def __init__(self, question_name: str | None = None) -> None:
        self.message = "Ошибка создания/обновления анкеты."
        if question_name:
            self.message += f" В вопросе `{question_name}` должно быть заполнено одно поле вопроса"


class QuestionnaireCreateUpdateMismatchError(Exception):
    def __init__(self, question_name: str | None = None) -> None:
        self.message = "Ошибка создания/обновления анкеты."
        if question_name:
            self.message += f" В вопросе `{question_name}` заполненное поле не соответствует его типу"


class QuestionnaireCreateUpdateNumberExistsError(Exception):
    def __init__(self, question_name: str | None = None) -> None:
        self.message = "Ошибка создания/обновления анкеты."
        if question_name:
            self.message += f"В опросе `{question_name}` повторяется порядковый номер"