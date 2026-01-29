from app.core import NotValidEntityException
from .consts import MIN_USER_AGE


class NotValidEmailException(NotValidEntityException):
    _MESSAGE = "Проверьте правильность введенного email"


class InvalidBirthDateException(NotValidEntityException):
    _MESSAGE = "Проверьте правильность введенной даты"


class FutureBirthDateException(NotValidEntityException):
    _MESSAGE = "Дата рождения не может быть в будущем"


class NotAllowedAgeException(NotValidEntityException):
    _MESSAGE = f"Возраст не подходит для регистрации. Вам должно быть не менее {MIN_USER_AGE} лет"
