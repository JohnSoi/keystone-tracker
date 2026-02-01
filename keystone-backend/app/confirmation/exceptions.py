"""Модуль исключений при подтверждении."""

from app.core import BadRequestException


class InvalidConfirmTokenException(BadRequestException):
    """Исключение при некорректном токене подтверждения."""

    _MESSAGE = "Токен подтверждения некорректен"


class TokenUsedException(BadRequestException):
    """Исключение использованного токена подтверждения."""

    _MESSAGE = "Токен подтверждения уже был использован"


class ExpiredConfirmationTokenException(BadRequestException):
    """Исключение при истечении срока действия токена подтверждения."""

    _MESSAGE = "Срок действия токена подтверждения истек. Пожалуйста, запросите новый токен."
