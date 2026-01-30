from app.core import NotValidEntityException, EntityConflictException, AuthException
from .consts import MIN_USER_AGE


class NotValidEmailException(NotValidEntityException):
    _MESSAGE = "Проверьте правильность введенного email"


class InvalidBirthDateException(NotValidEntityException):
    _MESSAGE = "Проверьте правильность введенной даты"


class FutureBirthDateException(NotValidEntityException):
    _MESSAGE = "Дата рождения не может быть в будущем"


class NotAllowedAgeException(NotValidEntityException):
    _MESSAGE = f"Возраст не подходит для регистрации. Вам должно быть не менее {MIN_USER_AGE} лет"

class LoginConflictException(EntityConflictException):
    def __init__(self, login: str) -> None:
        super().__init__(f'Логин "{login}" уже занят')


class EmailConflictException(EntityConflictException):
    def __init__(self, email: str) -> None:
        super().__init__(f'Email "{email}" уже занят')


class LoginNotFoundException(AuthException):
    def __init__(self, login: str) -> None:
        super().__init__(f'Пользователь с логином "{login}" не найден')


class PasswordIncorrectException(AuthException):
    _MESSAGE = "Неверный пароль. Попробуйте снова"