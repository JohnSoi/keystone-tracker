"""Модуль исключений для работы с пользователями."""

from app.core import AuthException, EntityConflictException, NotValidEntityException

from .consts import MIN_USER_AGE


class NotValidEmailException(NotValidEntityException):
    """Исключение для невалидного email."""

    _MESSAGE = "Проверьте правильность введенного email"


class InvalidBirthDateException(NotValidEntityException):
    """Исключение для невалидной даты рождения."""

    _MESSAGE = "Проверьте правильность введенной даты"


class FutureBirthDateException(NotValidEntityException):
    """Исключение для даты рождения в будущем."""

    _MESSAGE = "Дата рождения не может быть в будущем"


class NotAllowedAgeException(NotValidEntityException):
    """Исключение для возраста меньше минимального."""

    _MESSAGE = f"Возраст не подходит для регистрации. Вам должно быть не менее {MIN_USER_AGE} лет"


class LoginConflictException(EntityConflictException):
    """Исключение для логина, который уже занят."""

    def __init__(self, login: str) -> None:
        super().__init__(f'Логин "{login}" уже занят')


class EmailConflictException(EntityConflictException):
    """Исключение для email, который уже занят."""

    def __init__(self, email: str) -> None:
        super().__init__(f'Email "{email}" уже занят')


class LoginNotFoundException(AuthException):
    """Исключение для логина, которого нет в базе."""

    def __init__(self, login: str) -> None:
        super().__init__(f'Пользователь с логином "{login}" не найден')


class PasswordIncorrectException(AuthException):
    """Исключение для неверного пароля."""

    _MESSAGE = "Неверный пароль. Попробуйте снова"
