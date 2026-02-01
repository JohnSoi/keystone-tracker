"""Модуль исключений при работе с токенами доступа."""

from app.core import BadRequestException


class InvalidRestoreTokenException(BadRequestException):
    """Исключение для некорректного токена восстановления."""

    _MESSAGE = "Токен восстановления некорректен"


class TokenUsedException(BadRequestException):
    """Исключение для уже использованных токенов восстановления."""

    _MESSAGE = "Токен восстановления уже был использован"


class ExpiredRestoreTokenException(BadRequestException):
    """Исключение для истекшего токена восстановления."""

    _MESSAGE = "Срок действия токена восстановления истек. Пожалуйста, запросите новый токен восстановления."
