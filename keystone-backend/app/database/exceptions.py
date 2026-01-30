"""Модуль исключений при работе с БД."""

from app.core import BaseHttpException


class SessionNotCreatedException(BaseHttpException):
    """Исключение, возникающее при отсутствии сессии."""

    _MESSAGE = "Сессия для подключения к БД не создана"
