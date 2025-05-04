class AnswerOneChoiceCreateError:
    def __init__(self) -> None:
        self.message = "У вопроса с типом one_choice может быть только один вариант ответа"
