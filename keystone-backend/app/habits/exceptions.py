from app.core import NotValidEntityException
from app.habits.consts import DAYS_IN_WEEK


class InvalidColorTypeException(NotValidEntityException):
    _MESSAGE = "Значение цвета должно быть строкой в формате hex"


class InvalidColorValueException(NotValidEntityException):
    def __init__(self, color: str):
        self._MESSAGE = f"Значение {color} не является допустимым значением цвета"
        super().__init__()


class StartDateNoFutureException(NotValidEntityException):
    _MESSAGE = "Дата начала не может быть в будущем"


class EndDateBeforeStartDateException(NotValidEntityException):
    _MESSAGE = "Дата окончания не может быть раньше даты начала"


class EndDateNoPastException(NotValidEntityException):
    _MESSAGE = "Дата окончания не может быть в прошлом"


class InvalidDayOfWeekException(NotValidEntityException):
    _MESSAGE = "Список дней недели должен содержать только числа от 1 до 7"


class DuplicatesInDayOfWeekException(NotValidEntityException):
    _MESSAGE = "Список дней недели не может содержать повторяющиеся значения"


class InvalidDayInWeekException(NotValidEntityException):
    def __init__(self, day: int):
        self._MESSAGE = f"Номер дня недели {day} не является допустимым значением"
        super().__init__()


class TooManyDaysOfWeekException(NotValidEntityException):
    _MESSAGE = f"Количество дней недели не может быть больше {DAYS_IN_WEEK}"



