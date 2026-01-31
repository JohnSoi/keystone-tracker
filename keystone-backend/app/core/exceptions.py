"""Модуль базовых исключений приложения."""

from fastapi import HTTPException, status


class BaseHttpException(HTTPException):
    """
    Базовый класс исключений приложения. Все исключения приложения должны наследоваться от него.

    Attributes:
        _MESSAGE (str): Сообщение по умолчанию для исключения.
        _STATUS_CODE (int): Код статуса по умолчанию для исключения.
    """

    _STATUS_CODE: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _MESSAGE: str = "Внутренняя ошибка сервера"

    def __init__(self, message: str | None = None, status_code: int | None = None) -> None:
        """
        Инициализация исключения. Позволяет задать сообщение и код статуса исключения через конструктор.

        Args:
            message (str | None): Сообщение исключения. Если не задано, будет использовано значение по умолчанию.
            status_code (int | None): Код статуса исключения. Если не задано, будет использовано значение по умолчанию
        """
        super().__init__(detail=message or self._MESSAGE, status_code=status_code or self._STATUS_CODE)


class NotValidEntityException(BaseHttpException):
    """Исключение для некорректных данных в запросе."""

    _STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    _MESSAGE = "Некорректные данные в запросе"


class EntityConflictException(BaseHttpException):
    """Исключение для конфликта с существующей записью."""

    _STATUS_CODE = status.HTTP_409_CONFLICT
    _MESSAGE = "Запись уже существует"


class AuthException(BaseHttpException):
    """Исключение для авторизации."""

    _STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _MESSAGE = "Ошибка авторизации"


class NotFoundException(BaseHttpException):
    """Исключение для не найденных записей."""

    _STATUS_CODE = status.HTTP_404_NOT_FOUND
    _MESSAGE = "Запись не найдена"


class ForbiddenException(BaseHttpException):
    """Исключение для запрета доступа."""

    _STATUS_CODE = status.HTTP_403_FORBIDDEN
    _MESSAGE = "Доступ запрещен"


class BadRequestException(BaseHttpException):
    """Исключение для некорректных запросов."""

    _STATUS_CODE = status.HTTP_400_BAD_REQUEST
    _MESSAGE = "Некорректный запрос"
